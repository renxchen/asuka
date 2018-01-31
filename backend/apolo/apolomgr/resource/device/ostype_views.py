#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: ostype_views.py
@time: 2017/12/19 14:19
@desc:

"""

from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.models import Ostype
from backend.apolo.tools import constants
from rest_framework import viewsets
from backend.apolo.tools.views_helper import api_return
from django.core.paginator import Paginator
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
import simplejson as json
from django.db import transaction


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
        self.os_type_name = views_helper.get_request_value(self.request, 'name', method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        self.start_default_command = views_helper.get_request_value(self.request, 'start_default_command', method)
        self.end_default_command = views_helper.get_request_value(self.request, 'end_default_command', method)
        self.log_fail_judges = views_helper.get_request_value(self.request, 'log_fail_judges', method)
        self.status = views_helper.get_request_value(self.request, 'status', method)
        self.cli_error_context = views_helper.get_request_value(self.request, 'cli_error_context', method)
        self.cli_default_prompt = views_helper.get_request_value(self.request, 'cli_default_prompt', method)
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
            return exception_handler(e)

    def get(self):
        try:
            queryset = Ostype.objects.all()
            if self.id:
                query_conditions = {'ostypeid': self.id}
                queryset = Ostype.objects.filter(**query_conditions)
            serializer = OstypeSerializer(queryset, many=True)
            paginator = Paginator(serializer.data, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': contacts.object_list,
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
                data = {
                    'name': self.os_type_name,
                    'desc': self.desc,
                    'start_default_commands': self.start_default_command,
                    'end_default_commands': self.end_default_command,
                    'log_fail_judges': self.log_fail_judges,
                    'status': self.status,
                    'cli_error_context': self.cli_error_context,
                    'cli_default_prompt': self.cli_default_prompt,
                    'telnet_prompt': self.telnet_prompt,
                    'telnet_timeout': int(self.telnet_timeout),
                    'snmp_timeout': int(self.snmp_timeout),
                }
                if self.os_type_name is not '':
                    get_name_from_cp = self.get_ostype(**{'name': self.os_type_name})
                    if not isinstance(get_name_from_cp, str):
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.OSTYPE_EXIST_IN_SCHEDULE
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
                if self.id:
                    data = {
                        'name': self.os_type_name,
                        'desc': self.desc,
                        'start_default_commands': self.start_default_command,
                        'end_default_commands': self.end_default_command,
                        'log_fail_judges': self.log_fail_judges,
                        'status': self.status,
                        'cli_error_context': self.cli_error_context,
                        'cli_default_prompt': self.cli_default_prompt,
                        'telnet_prompt': self.telnet_prompt,
                        'telnet_timeout': int(self.telnet_timeout),
                        'snmp_timeout': int(self.snmp_timeout),
                    }
                    if self.os_type_name is not '':
                        get_name_from_cp = self.get_ostype(**{'name': self.os_type_name})
                        if not isinstance(get_name_from_cp, str):
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.OSTYPE_EXIST_IN_SCHEDULE
                                }
                            }
                            return api_return(data=data)
                    queryset = self.get_ostype(**{'ostypeid': self.id})
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
