# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: ostype_views.py
@time: 2017/03/04 14:19
@desc:

"""

from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.models import Ostype,Devices,Schedules,CollPolicy
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
        try:
            ostype_info = Ostype.objects.get(**kwargs)
            return ostype_info
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    def get(self):
        try:
            if self.id:
                queryset = Ostype.objects.filter(ostypeid=int(self.id))
                serializer = OstypeSerializer(queryset, many=True)
                data = {
                    'data': serializer.data,
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
                    'name':self.os_type_name,
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
        try:
            with transaction.atomic():
                if len(self.start_default_command) != 0:
                    start_default_commands = ''
                    for i in self.start_default_command:
                        cli_start = unicode(i.get('name'))
                        for x in cli_start:
                            if not (str(x).isalnum() or str(x) in string.punctuation or x == ' '):
                                message = "END_DEFAULT_COMMANDS_ERROR"
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: message
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
                                message = "END_DEFAULT_COMMANDS_ERROR"
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: message
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
                            message = "LOG_FAIL_JUDGES_ERROR"
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: message
                                }
                            }
                            return api_return(data=data)
                        else:
                            cli_error_context += cli_error + u'，'
                    cli_error_context = cli_error_context[:-1]
                else:
                    cli_error_context = None
                if self.telnet_prompt == '':
                    message = "TELNET_PROMPT_EMPTY_ERROR"
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: message
                        }
                    }
                    return api_return(data=data)
                else:
                    try:
                        re.compile(self.telnet_prompt)
                    except Exception, e:
                        message = "TELNET_PROMPT_FORMAT_ERROR"
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: message
                            }
                        }
                        return api_return(data=data)
                try:
                    telnet_timeout = int(self.telnet_timeout)
                except Exception, e:
                    message = "TELNET_TIMEOUT_FORMAT_ERROR"
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: message
                        }
                    }
                    return api_return(data=data)
                try:
                    snmp_timeout = int(self.snmp_timeout)
                except Exception, e:
                    message = "SNMP_TIMEOUT_FORMAT_ERROR"
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: message
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
                        message = "NAME_IS_EXISTENCE"
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: message,
                            }
                        }
                        return api_return(data=data)
                else:
                    message = "NAME_IS_EMPTY"
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: message,
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
        try:
            with transaction.atomic():
                if self.ostypeid:
                    if len(self.start_default_command) != 0:
                        start_default_commands = ''
                        for i in self.start_default_command:
                            cli_start = unicode(i.get('name'))
                            for x in cli_start:
                                if not (str(x).isalnum() or str(x) in string.punctuation or x == ' '):
                                    message = "END_DEFAULT_COMMANDS_ERROR"
                                    data = {
                                        'new_token': self.new_token,
                                        constants.STATUS: {
                                            constants.STATUS: constants.FALSE,
                                            constants.MESSAGE: message
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
                                    message = "END_DEFAULT_COMMANDS_ERROR"
                                    data = {
                                        'new_token': self.new_token,
                                        constants.STATUS: {
                                            constants.STATUS: constants.FALSE,
                                            constants.MESSAGE: message
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
                                message = "LOG_FAIL_JUDGES_ERROR"
                                data = {
                                    'new_token': self.new_token,
                                    constants.STATUS: {
                                        constants.STATUS: constants.FALSE,
                                        constants.MESSAGE: message
                                    }
                                }
                                return api_return(data=data)
                            else:
                                cli_error_context += cli_error + u'，'
                        cli_error_context = cli_error_context[:-1]
                    else:
                        cli_error_context = None
                    if self.telnet_prompt == '':
                        message = "TELNET_PROMPT_EMPTY_ERROR"
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: message
                            }
                        }
                        return api_return(data=data)
                    else:
                        try:
                            re.compile(self.telnet_prompt)
                        except Exception, e:
                            message = "TELNET_PROMPT_FORMAT_ERROR"
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: message
                                }
                            }
                            return api_return(data=data)
                    try:
                        telnet_timeout = int(self.telnet_timeout)
                    except Exception, e:
                        message = "TELNET_TIMEOUT_FORMAT_ERROR"
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: message
                            }
                        }
                        return api_return(data=data)
                    try:
                        snmp_timeout = int(self.snmp_timeout)
                    except Exception, e:
                        message = "SNMP_TIMEOUT_FORMAT_ERROR"
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: message
                            }
                        }
                        return api_return(data=data)
                    data = {
                        'name': self.os_type_name,
                        'desc': self.desc,
                        'start_default_commands': start_default_commands[:-1],
                        'end_default_commands': end_default_commands[:-1],
                        'log_fail_judges': cli_error_context,
                        'status': self.status,
                        'telnet_prompt': self.telnet_prompt,
                        'telnet_timeout': telnet_timeout,
                        'snmp_timeout': snmp_timeout,
                    }
                    if self.os_type_name.strip() == '':
                        message = "NAME_IS_EMPTY"
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: message,
                            }
                        }
                        return api_return(data=data)
                    queryset = self.get_ostype(**{'ostypeid': self.ostypeid})
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
                        devices_queryset = Devices.objects.filter(ostype_id=self.id)
                        if len(devices_queryset) != 0:
                            message = "EXIST_IN_DEVICES"
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: message
                                }
                            }
                            return api_return(data=data)
                        schedules_queryset = Schedules.objects.filter(ostype_id=self.id)
                        if len(schedules_queryset) != 0:
                            message = "EXIST_IN_SCHEDULE"
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: message
                                }
                            }
                            return api_return(data=data)
                        coll_policy_queryset = CollPolicy.objects.filter(ostype_id=self.id)
                        if len(coll_policy_queryset) != 0:
                            message = "EXIST_IN_COLL_POLICY"
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
