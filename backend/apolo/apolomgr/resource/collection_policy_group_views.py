#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: collection_policy_views.py
@time: 2017/12/14 14:39
@desc:

'''

from backend.apolo.serializer.collection_policy_serializer import CollPolicyGroupSerializer, PolicyGroupSerializer
from backend.apolo.models import CollPolicyGroups, PolicysGroups
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.common import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback
import time
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class CollPolicyGroupViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollPolicyGroupViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'HTTP_FROM', 'META')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'HTTP_MAX', 'META')
        self.id = views_helper.get_request_value(self.request, 'group_id', 'BODY')
        self.name = views_helper.get_request_value(self.request, 'group_name', 'BODY')
        self.desc = views_helper.get_request_value(self.request, 'group_desc', 'BODY')
        self.ostype = views_helper.get_request_value(self.request, 'ostype', 'BODY')

    @staticmethod
    def get_cp_group(**kwargs):
        try:
            return CollPolicyGroups.objects.get(**kwargs)
        except CollPolicyGroups.DoesNotExist:
            return False

    @staticmethod
    def get_policy_group(**kwargs):
        try:
            return PolicysGroups.objects.filter(**kwargs)
        except PolicysGroups.DoesNotExist:
            return False

    def del_policy_group(self, **kwargs):
        try:
            queryset_related = self.get_policy_group(**kwargs)
            return queryset_related.delete()
        except PolicysGroups.DoesNotExist:
            return False

    def get(self):
        # http://127.0.0.1:1111/v1/api_collection_policy_group/
        try:
            field_relation_ships = {
                'id': 'policy_group_id',
                'name': 'name',
                'desc': 'desc',
                'ostype': 'ostype__name',
            }
            # http://127.0.0.1:1111/v1/api_collection_policy_group/?sort_by=name&order=asc&name=test&ostype=CISCO&desc=&search_fields=name,ostype,desc
            query_data = {
                'name': self.name,
                'desc': self.desc,
                'ostype__name': self.ostype,
            }
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data)
            if search_conditions:
                queryset = CollPolicyGroups.objects.filter(**search_conditions).order_by(*sorts)
            else:
                queryset = CollPolicyGroups.objects.all()
                if self.id is not '':
                    queryset = CollPolicyGroups.objects.filter(policy_group_id=self.id)
            serializer = CollPolicyGroupSerializer(queryset, many=True)
            paginator = Paginator(serializer.data, self.max_size_per_page)
            contacts = paginator.page(self.page_from)
            data = {'data': contacts.object_list, 'new_token': self.new_token, 'num_page': paginator.num_pages,
                    'page_range': list(paginator.page_range), 'page_has_next': contacts.has_next(),
                    'current_page_num': contacts.number}
            return api_return(message={constants.STATUS: constants.TRUE, constants.MESSAGE: constants.SUCCESS},
                              data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        # http://127.0.0.1:1111/v1/api_collection_policy_group/
        # {
        #     "group_id": 1,
        #     "group_name": "test",
        #     "group_desc": "test",
        #     "ostype": 1,
        #     "cps": [{"status": 1, "collection_policy_id": 1, "exec_interval": 1, "expired_duration": 1},
        #             {"status": 1, "collection_policy_id": 3, "exec_interval": 1, "expired_duration": 1}]
        #
        # }
        try:
            data = {
                'name': self.name,
                'desc': self.desc,
                'ostype': self.ostype,
            }
            cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
            serializer = CollPolicyGroupSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                for per_cp in cps:
                    per_cp['policy_group'] = int(serializer.data.get('policy_group_id'))
                    per_cp['history'] = time.time()
                    per_cp['policy'] = per_cp['collection_policy_id']
                    # data = JSONParser().parse(self.request)
                    serializer_related = PolicyGroupSerializer(data=per_cp)
                    if serializer_related.is_valid():
                        serializer_related.save()
                    else:
                        data = {'data': serializer_related.errors, 'new_token': self.new_token}
                        return api_return(
                            message={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.FAILED},
                            data=data)
                return api_return(message={constants.STATUS: constants.TRUE, constants.MESSAGE: constants.SUCCESS})
            else:
                data = {'data': serializer.errors, 'new_token': self.new_token}
                return api_return(message={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.FAILED},
                                  data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        # http://127.0.0.1:1111/v1/api_collection_policy_group/
        # {
        #     "group_id": 1,
        #     "group_name": "test",
        #     "group_desc": "test",
        #     "ostype": 1,
        #     "cps": [{"status": 1, "collection_policy_id": 6, "exec_interval": 1, "expired_duration": 1},
        #             {"status": 1, "collection_policy_id": 7, "exec_interval": 1, "expired_duration": 1}]
        #
        # }
        try:
            cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
            kwargs = {'policy_group_id': self.id}
            queryset = self.get_cp_group(**kwargs)
            data = {
                'name': self.name,
                'desc': self.desc,
                'ostype': self.ostype,
            }
            if queryset is False:
                message = 'There is no result for current query.'
                data = {'data': message, 'new_token': self.new_token}
                return api_return(message={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.FAILED},
                                  data=data)
            queryset_related = self.get_policy_group(**kwargs)
            if queryset_related is False:
                message = 'There is no result for current query.'
                data = {'data': message, 'new_token': self.new_token}
                return api_return(message={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.FAILED},
                                  data=data)
            self.del_policy_group(**kwargs)
            for per_cp in cps:
                per_cp['policy_group'] = int(self.id)
                per_cp['history'] = time.time()
                per_cp['policy'] = per_cp['collection_policy_id']
                serializer_related = PolicyGroupSerializer(data=per_cp)
                if serializer_related.is_valid():
                    serializer_related.save()
                else:
                    data = {'data': serializer_related.errors, 'new_token': self.new_token}
                    return api_return(
                        message={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.FAILED},
                        data=data)
            return api_return(message={constants.STATUS: constants.TRUE, constants.MESSAGE: constants.SUCCESS})
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        # http://127.0.0.1:1111/v1/api_collection_policy_group/?id=5
        try:
            kwargs = {'policy_group_id': self.id}
            queryset = self.get_cp_group(**kwargs)
            if queryset is False:
                message = 'There is no result for current query.'
                data = {'data': message, 'new_token': self.new_token}
                return api_return(
                    message={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.FAILED},
                    data=data)
            queryset.delete()
            data = {'new_token': self.new_token}
            return api_return(message={constants.STATUS: constants.TRUE, constants.MESSAGE: constants.SUCCESS},
                              data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)
