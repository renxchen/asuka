#!/usr/bin/env python
"""

@author: necwang
@contact: necwang@cisco.com
@file: common_views.py
@time: 2017/12/19 14:19
@desc:

"""

from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.serializer.devices_groups_serializer import GroupsSerializer
from backend.apolo.models import Ostype, CollPolicy, Groups
from backend.apolo.tools import constants
from rest_framework import viewsets
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler


class OsTypeViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(OsTypeViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')

    def get(self):
        try:
            queryset = Ostype.objects.all()
            if self.id:
                query_conditions = {'ostypeid': self.id}
                queryset = Ostype.objects.filter(**query_conditions)
            serializer = OstypeSerializer(queryset, many=True)
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
            print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class CollPolicyViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollPolicyViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')

    def get(self):
        try:
            queryset = CollPolicy.objects.all().values('coll_policy_id', 'value_type', 'name', 'policy_type')
            if self.id != '':
                queryset = CollPolicy.objects.filter(ostype=self.id).values('coll_policy_id', 'value_type', 'name',
                                                                            'policy_type')
            # serializer = CollPolicyNameSerializer(queryset, many=True)
            for per in queryset:
                if per['policy_type'] == 1:
                    # SNMP
                    per['name'] = '[SNMP]' + per['name']
                else:
                    # CLI
                    per['name'] = '[CLI]' + per['name']
            data = {
                'data': list(queryset),
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class DeviceGroupViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DeviceGroupViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.device_group_id = views_helper.get_request_value(self.request, 'id', 'GET')

    def get(self):
        try:
            queryset = Groups.objects.all()
            if self.device_group_id:
                query_conditions = {'group_id': self.device_group_id}
                queryset = Groups.objects.filter(**query_conditions)
            serializer = GroupsSerializer(queryset, many=True)
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
            print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
