# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: ostype_views.py
@time: 2018/03/04 14:19
@desc:

"""

from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.models import Ostype, Devices, Schedules, CollPolicy, Groups, CollPolicyGroups
from backend.apolo.tools import constants
from rest_framework import viewsets
from backend.apolo.tools.views_helper import api_return
from django.core.paginator import Paginator
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
import simplejson as json
from django.db import transaction
import string, re


class OsTypeViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(OsTypeViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        method = 'GET'
        if request.method.lower() == 'get':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        # ostype related parameters
        self.ostypeid = views_helper.get_request_value(self.request, 'ostypeid', method)
        self.os_type_name = views_helper.get_request_value(self.request, 'name', method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        self.start_default_command = views_helper.get_request_value(self.request, 'start_default_commands', method)
        self.end_default_command = views_helper.get_request_value(self.request, 'end_default_commands', method)
        self.log_fail_judges = views_helper.get_request_value(self.request, 'log_fail_judges', method)
        self.status = views_helper.get_request_value(self.request, 'status', method)
        self.telnet_prompt = views_helper.get_request_value(self.request, 'telnet_prompt', method)
        self.telnet_timeout = views_helper.get_request_value(self.request, 'telnet_timeout', method)
        self.snmp_timeout = views_helper.get_request_value(self.request, 'snmp_timeout', method)

    @staticmethod
    def get_ostype(**kwargs):
        """@brief
        get the data of the Ostype table
        @param kwargs: the condition to query the table
        @pre call when need to get the data of Ostype table
        @post return the data when queryset exits and exception string when queryset not exit
        @return: the data when queryset exits and exception string when queryset not exit
        """
        try:
            ostype_info = Ostype.objects.get(**kwargs)
            return ostype_info
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def get(self):
        """@brief
        get the data of Ostype table
        @return: the data of Ostype table
        """
        try:
            if self.id:
                # return verify field for name
                queryset_devices = Devices.objects.filter(ostype_id=self.id)
                queryset_groups = Groups.objects.filter(ostype_id=self.id)
                schedules_queryset = Schedules.objects.filter(ostype_id=self.id)
                coll_policy_queryset = CollPolicy.objects.filter(ostype_id=self.id)
                coll_policy_groups = CollPolicyGroups.objects.filter(ostypeid=self.id)
                if queryset_devices.exists() or queryset_groups.exists() or schedules_queryset.exists() \
                        or coll_policy_groups.exists() or coll_policy_queryset.exists():
                    name = False
                else:
                    name = True
                queryset = Ostype.objects.filter(ostypeid=int(self.id))
                serializer = OstypeSerializer(queryset, many=True)
                data = {
                    'data': serializer.data,
                    'verify_result': {
                        "name": name
                    },
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                }
            else:
                field_relation_ships = {
                    'name': 'name',
                    'log_fail_judges': 'log_fail_judges',
                    'status': 'status',
                    'snmp_timeout': 'snmp_timeout',
                    'telnet_timeout': 'telnet_timeout',
                    'telnet_prompt': 'telnet_prompt',
                    'start_default_commands': 'start_default_commands',
                    'end_default_commands': 'end_default_commands',
                    'desc': 'desc',
                }
                query_data = {
                    'name': self.os_type_name,
                    'log_fail_judges': self.log_fail_judges,
                    'status': self.status,
                    'snmp_timeout': self.snmp_timeout,
                    'telnet_timeout': self.telnet_timeout,
                    'telnet_prompt': self.telnet_prompt,
                    'start_default_commands': self.start_default_command,
                    'end_default_commands': self.end_default_command,
                    'desc': self.desc,
                }
                search_fields = ['name', 'log_fail_judges', 'status', 'snmp_timeout', 'telnet_timeout', 'telnet_prompt',
                                 'start_default_commands', 'end_default_commands', 'desc']
                sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                              query_data, search_fields)
                if len(sorts) == 0:
                    sorts = ['ostypeid']
                if search_conditions:
                    queryset = Ostype.objects.filter(**search_conditions).order_by(*sorts)
                else:
                    queryset = Ostype.objects.all().order_by(*sorts)
                paginator = Paginator(queryset, int(self.max_size_per_page))
                contacts = paginator.page(int(self.page_from))
                serializer = OstypeSerializer(contacts.object_list, many=True)
                data = {
                    'data': serializer.data,
                    'new_token': self.new_token,
                    'num_page': paginator.num_pages,
                    'page_range': list(paginator.page_range),
                    'page_has_next': contacts.has_next(),
                    'total_num': len(queryset),
                    'current_page_num': contacts.number,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        """@brief
        create a ostype
        @return: the created ostype when create success and error when create fail
        """
        try:
            with transaction.atomic():
                if len(self.start_default_command) != 0:
                    start_default_commands = ''
                    for i in self.start_default_command:
                        cli_start = unicode(i.get('name'))
                        for x in cli_start:
                            if not (str(x).isalnum() or str(x) in string.punctuation or x == ' '):
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: constants.START_DEFAULT_COMMANDS_ERROR
                                    }
                                }
                                return api_return(data=data)
                        start_default_commands = start_default_commands + cli_start + u'，'
                else:
                    start_default_commands = None
                if len(self.end_default_command) != 0:
                    end_default_commands = ''
                    for i in self.end_default_command:
                        cli_end = i.get('name')
                        for x in cli_end:
                            if not (str(x).isalnum() or str(x) in string.punctuation or x == ' '):
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: constants.END_DEFAULT_COMMANDS_ERROR
                                    }
                                }
                                return api_return(data=data)
                        end_default_commands += cli_end + u'，'
                else:
                    end_default_commands = None
                if len(self.log_fail_judges) != 0:
                    cli_error_context = ''
                    for i in self.log_fail_judges:
                        cli_error = i.get('name')
                        try:
                            re.compile(cli_error)
                        except Exception, e:
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.LOG_FAIL_JUDGES_ERROR
                                }
                            }
                            return api_return(data=data)
                        else:
                            cli_error_context += cli_error + u'，'
                    cli_error_context = cli_error_context[:-1]
                else:
                    cli_error_context = None
                if self.telnet_prompt == '':
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.TELNET_PROMPT_EMPTY_ERROR
                        }
                    }
                    return api_return(data=data)
                else:
                    try:
                        re.compile(self.telnet_prompt)
                    except Exception, e:
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.TELNET_PROMPT_FORMAT_ERROR
                            }
                        }
                        return api_return(data=data)
                try:
                    telnet_timeout = int(self.telnet_timeout)
                except Exception, e:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.TELNET_TIMEOUT_FORMAT_ERROR
                        }
                    }
                    return api_return(data=data)
                try:
                    snmp_timeout = int(self.snmp_timeout)
                except Exception, e:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.SNMP_TIMEOUT_FORMAT_ERROR
                        }
                    }
                    return api_return(data=data)
                if start_default_commands is not None:
                    start_default_commands = start_default_commands[:-1]
                if end_default_commands is not None:
                    end_default_commands = end_default_commands[:-1]
                data = {
                    'name': self.os_type_name,
                    'desc': self.desc,
                    'start_default_commands': start_default_commands,
                    'end_default_commands': end_default_commands,
                    'log_fail_judges': cli_error_context,
                    'status': self.status,
                    'telnet_prompt': self.telnet_prompt,
                    'telnet_timeout': telnet_timeout,
                    'snmp_timeout': snmp_timeout,
                }
                if self.os_type_name is not '':
                    get_name_from_cp = self.get_ostype(**{'name': self.os_type_name})
                    if not isinstance(get_name_from_cp, str):
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.OSTYPE_NAME_EXISTS,
                            }
                        }
                        return api_return(data=data)
                else:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.OSTYPE_NAME_EMPTY,
                        }
                    }
                    return api_return(data=data)
                serializer = OstypeSerializer(data=data)
                if serializer.is_valid(Exception):
                    serializer.save()
                    data = {
                        'data': serializer.data,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        """@brief
        modify a ostype
        @return: the modified ostype when modify success and error when modify fail
        """
        try:
            with transaction.atomic():
                if self.ostypeid:
                    if len(self.start_default_command) != 0:
                        start_default_commands = ''
                        for i in self.start_default_command:
                            cli_start = unicode(i.get('name'))
                            for x in cli_start:
                                if not (str(x).isalnum() or str(x) in string.punctuation or x == ' '):
                                    data = {
                                        'new_token': self.new_token,
                                        constants.STATUS: {
                                            constants.STATUS: constants.FALSE,
                                            constants.MESSAGE: constants.START_DEFAULT_COMMANDS_ERROR
                                        }
                                    }
                                    return api_return(data=data)
                            start_default_commands = start_default_commands + cli_start + u'，'
                    else:
                        start_default_commands = None
                    if len(self.end_default_command) != 0:
                        end_default_commands = ''
                        for i in self.end_default_command:
                            cli_end = i.get('name')
                            for x in cli_end:
                                if not (str(x).isalnum() or str(x) in string.punctuation or x == ' '):
                                    data = {
                                        'new_token': self.new_token,
                                        constants.STATUS: {
                                            constants.STATUS: constants.FALSE,
                                            constants.MESSAGE: constants.END_DEFAULT_COMMANDS_ERROR
                                        }
                                    }
                                    return api_return(data=data)
                            end_default_commands += cli_end + u'，'
                    else:
                        end_default_commands = None
                    if len(self.log_fail_judges) != 0:
                        cli_error_context = ''
                        for i in self.log_fail_judges:
                            cli_error = i.get('name')
                            try:
                                re.compile(cli_error)
                            except Exception, e:
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: constants.LOG_FAIL_JUDGES_ERROR
                                    }
                                }
                                return api_return(data=data)
                            else:
                                cli_error_context += cli_error + u'，'
                        cli_error_context = cli_error_context[:-1]
                    else:
                        cli_error_context = None
                    if self.telnet_prompt == '':
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.TELNET_PROMPT_EMPTY_ERROR
                            }
                        }
                        return api_return(data=data)
                    else:
                        try:
                            re.compile(self.telnet_prompt)
                        except Exception, e:
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.TELNET_PROMPT_FORMAT_ERROR
                                }
                            }
                            return api_return(data=data)
                    try:
                        telnet_timeout = int(self.telnet_timeout)
                    except Exception, e:
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.TELNET_TIMEOUT_FORMAT_ERROR
                            }
                        }
                        return api_return(data=data)
                    try:
                        snmp_timeout = int(self.snmp_timeout)
                    except Exception, e:
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.SNMP_TIMEOUT_FORMAT_ERROR
                            }
                        }
                        return api_return(data=data)
                    if start_default_commands is not None:
                        start_default_commands = start_default_commands[:-1]
                    if end_default_commands is not None:
                        end_default_commands = end_default_commands[:-1]
                    data = {
                        'name': self.os_type_name,
                        'desc': self.desc,
                        'start_default_commands': start_default_commands,
                        'end_default_commands': end_default_commands,
                        'log_fail_judges': cli_error_context,
                        'status': self.status,
                        'telnet_prompt': self.telnet_prompt,
                        'telnet_timeout': telnet_timeout,
                        'snmp_timeout': snmp_timeout,
                    }
                    queryset = self.get_ostype(**{'ostypeid': self.ostypeid})
                    if self.os_type_name.strip() == '':
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.OSTYPE_NAME_EMPTY,
                            }
                        }
                        return api_return(data=data)
                    else:
                        ostype_database = self.get_ostype(**{"name": self.os_type_name})
                        if not isinstance(ostype_database, str):
                            if ostype_database.ostypeid != self.ostypeid:
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: constants.OSTYPE_NAME_EXISTS,
                                    }
                                }
                                return api_return(data=data)
                    serializer = OstypeSerializer(queryset, data=data)
                    if serializer.is_valid(Exception):
                        serializer.save()
                        data = {
                            'data': serializer.data,
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.TRUE,
                                constants.MESSAGE: constants.SUCCESS
                            }
                        }
                        return api_return(data=data)

        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        """@brief
        delete a ostype
        @return: the success when delete success and error when delete fail
        """
        try:
            with transaction.atomic():
                if self.id:
                    queryset = self.get_ostype(**{'ostypeid': self.id})
                    if isinstance(queryset, str):
                        if json.loads(queryset)['message'] is not '':
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: json.loads(queryset)['message']
                                }
                            }
                            return api_return(data=data)
                    else:
                        message = ''
                        devices_queryset = Devices.objects.filter(ostype_id=self.id)
                        if devices_queryset.exists():
                            message += constants.OSTYPE_EXIST_IN_DEVICES + "<br/>"
                        queryset_groups = Groups.objects.filter(ostype_id=self.id)
                        if queryset_groups.exists():
                            message += constants.OSTYPE_EXIST_IN_DEVICEGROUPS + "<br/>"
                        schedules_queryset = Schedules.objects.filter(ostype_id=self.id)
                        if schedules_queryset.exists():
                            message += constants.OSTYPE_EXIST_IN_SCHEDULE2 + "<br/>"
                        coll_policy_queryset = CollPolicy.objects.filter(ostype_id=self.id)
                        if coll_policy_queryset.exists():
                            message += constants.OSTYPE_EXISTS_IN_COLL_POLICY + "<br/>"
                        coll_policy_groups = CollPolicyGroups.objects.filter(ostypeid=self.id)
                        if coll_policy_groups.exists():
                            message += constants.OSTYPE_EXIST_IN_COLL_POLICY_GROUPS + "<br/>"
                        if message != '':
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: message
                                }
                            }
                            return api_return(data=data)
                        queryset.delete()
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.TRUE,
                                constants.MESSAGE: constants.SUCCESS
                            }
                        }
                        return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
