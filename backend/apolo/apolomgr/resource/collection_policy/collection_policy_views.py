#!/usr/bin/env python

"""

@author: kimli
@contact: kimli@cisco.com
@file: collection_policy_views.py
@time: 2017/12/14 14:39
@desc:

"""
from backend.apolo.serializer.collection_policy_serializer import CollPolicySerializer
from backend.apolo.models import CollPolicy
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback


class CollPolicyViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollPolicyViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.name = views_helper.get_request_value(self.request, 'name', 'GET')
        self.ostype = views_helper.get_request_value(self.request, 'ostype', 'GET')
        self.cli_command = views_helper.get_request_value(self.request, 'cli_command', 'GET')
        self.desc = views_helper.get_request_value(self.request, 'desc', 'GET')
        self.snmp_oid = views_helper.get_request_value(self.request, 'snmp_oid', 'GET')
        self.policy_type = views_helper.get_request_value(self.request, 'policy_type', 'GET')

    @staticmethod
    def get_cp(**kwargs):
        try:
            return CollPolicy.objects.get(**kwargs)
        except CollPolicy.DoesNotExist:
            return False

    def get(self):
        # http://127.0.0.1:1111/v1/api_collection_policy/?id=1
        try:
            if self.id is not '':
                queryset = CollPolicy.objects.filter(**{'coll_policy_id': self.id})
                serializer = CollPolicySerializer(queryset, many=True)
                data = {
                    'data': serializer.data,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                # get tree information
                return api_return(data=data)
            field_relation_ships = {
                'id': 'id',
                'name': 'name',
                'desc': 'desc',
                'cli_command': 'cli_command',
                'ostype': 'ostype__name',
                'snmp_oid': 'snmp_oid',
                'policy_type': 'policy_type',
            }
            # http://127.0.0.1:1111/v1/api_collection_policy/?page=1&rows=5&sidx=name&sord=asc&name=TEST&ostype=CISCO&cli_command=clock&desc=&policy_type=1
            query_data = {
                'name': self.name,
                'desc': self.desc,
                'cli_command': self.cli_command,
                'ostype__name': self.ostype,
                'snmp_oid': self.snmp_oid,
                'policy_type': self.policy_type,
            }
            search_fields = ['name', 'ostype', 'cli_command', 'desc', 'snmp_oid']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            total_num = len(CollPolicy.objects.filter(**{'policy_type': self.policy_type}))
            if search_conditions:
                queryset = CollPolicy.objects.filter(**search_conditions).order_by(*sorts)
            else:
                queryset = CollPolicy.objects.filter(**{'policy_type': self.policy_type}).order_by(*sorts)
                if self.id is not '':
                    queryset = CollPolicy.objects.filter(coll_policy_id=self.id)
            serializer = CollPolicySerializer(queryset, many=True)
            paginator = Paginator(serializer.data, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': contacts.object_list,
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                'page_range': list(paginator.page_range),
                'page_has_next': contacts.has_next(),
                'total_num': total_num,
                'current_page_num': contacts.number,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        # http://127.0.0.1:1111/v1/api_collection_policy/?name=test_cp_cli&desc=Cisco IOS XE_cli&ostype=1&cli_command=show interface_cli&policy_type=0
        # http://127.0.0.1:1111/v1/api_collection_policy/?name=test_cp_snmp&desc=Cisco IOS XE_snmp&ostype=1&snmp_oid=1.3.6.1.2.1.1&policy_type=1

        try:
            data = {
                'name': self.name,
                'desc': self.desc,
                'cli_command': self.cli_command,
                'ostype': self.ostype,
                'snmp_oid': self.snmp_oid,
                'policy_type': self.policy_type
            }
            serializer = CollPolicySerializer(data=data)
            if serializer.is_valid():
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
            else:
                data = {
                    'data': serializer.errors,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.FAILED
                    }
                }
                return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        # http://127.0.0.1:1111/v1/api_collection_policy/?id=2&name=MIYAZAKI-morning-shot-update&desc=&ostype=1&cli_command=show interface
        # http://127.0.0.1:1111/v1/api_collection_policy/?id=2&name=MIYAZAKI-morning-shot-update&desc=&ostype=1&snmp_oid=1.3.6.1.2.1.1
        try:
            kwargs = {'coll_policy_id': self.id}
            queryset = self.get_cp(**kwargs)
            data = {
                'name': self.name,
                'desc': self.desc,
                'cli_command': self.cli_command,
                'ostype': self.ostype,
                'snmp_oid': self.snmp_oid
            }
            if queryset is False:
                message = 'There is no result for current query.'
                data = {
                    'data': message,
                    'new_token': self.new_token,
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.FAILED
                }
                return api_return(data=data)
            serializer = CollPolicySerializer(queryset, data=data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'data': serializer.data,
                    'new_token': self.new_token,
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
                return api_return(data=data)
            else:
                data = {
                    'data': serializer.errors,
                    'new_token': self.new_token,
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.FAILED
                }
                return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        # http://127.0.0.1:1111/v1/api_collection_policy/?id=4
        try:
            kwargs = {'coll_policy_id': self.id}
            queryset = self.get_cp(**kwargs)
            if queryset is False:
                message = 'There is no result for current query.'
                data = {
                    'data': message,
                    'new_token': self.new_token,
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.FAILED
                }
                return api_return(data=data)
            queryset.delete()
            data = {
                'new_token': self.new_token,
                constants.STATUS: constants.TRUE,
                constants.MESSAGE: constants.SUCCESS
            }
            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)
