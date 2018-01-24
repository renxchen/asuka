#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: collection_policy_views.py
@time: 2017/12/14 14:39
@desc:

'''

from backend.apolo.serializer.collection_policy_serializer import CollPolicyGroupSerializer, PolicyGroupSerializer
from backend.apolo.models import CollPolicyGroups, PolicysGroups, Schedules
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback
import time
from django.db import transaction
import simplejson as json


class CollPolicyGroupViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollPolicyGroupViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.name = views_helper.get_request_value(self.request, 'name', 'GET')
        self.desc = views_helper.get_request_value(self.request, 'desc', 'GET')
        self.ostype = views_helper.get_request_value(self.request, 'ostype', 'GET')

    @staticmethod
    def get_cp_group(**kwargs):
        try:
            cps = CollPolicyGroups.objects.filter(**kwargs)
            return cps
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_policy_group(**kwargs):
        try:
            pg = PolicysGroups.objects.filter(**kwargs)
            if len(pg) > 0:
                return pg
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def del_policy_group(self, **kwargs):
        try:
            pg = self.get_policy_group(**kwargs)
            if pg is not None:
                return pg.delete()
            else:
                return False
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_schedule(**kwargs):
        try:
            detail = Schedules.objects.filter(**kwargs)
            if len(detail) > 0:
                return False
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def get(self):
        try:
            if self.id is not '':
                queryset = CollPolicyGroups.objects.filter(**{'policy_group_id': self.id})
                queryset_pg = PolicysGroups.objects.filter(**{'policy_group_id': self.id})
                serializer = CollPolicyGroupSerializer(queryset, many=True)
                serializer_pg = PolicyGroupSerializer(queryset_pg, many=True)
                paginator = Paginator(serializer_pg.data, self.max_size_per_page)
                contacts = paginator.page(self.page_from)
                total_related_num = len(PolicysGroups.objects.all())
                data = {
                    'policys_groups_data': contacts.object_list,
                    'num_page': paginator.num_pages,
                    'page_range': list(paginator.page_range),
                    'page_has_next': contacts.has_next(),
                    'total_num': total_related_num,
                    'current_page_num': contacts.number,
                    'new_token': self.new_token,
                    'policy_group_data': serializer.data,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS,
                    },
                }
                return api_return(data=data)
            field_relation_ships = {
                'id': 'policy_group_id',
                'name': 'name',
                'desc': 'desc',
                'ostypeid': 'ostype__name',
            }
            query_data = {
                'name': self.name,
                'desc': self.desc,
                'ostype__name': self.ostype,
            }
            search_fields = ['name', 'ostype', 'desc']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            total_num = len(CollPolicyGroups.objects.all())
            if search_conditions:
                queryset = CollPolicyGroups.objects.filter(**search_conditions).order_by(*sorts)
            else:
                queryset = CollPolicyGroups.objects.all().order_by(*sorts)
            serializer = CollPolicyGroupSerializer(queryset, many=True)
            paginator = Paginator(serializer.data, self.max_size_per_page)
            contacts = paginator.page(self.page_from)
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
        try:
            with transaction.atomic():
                data = {
                    'name': self.name,
                    'desc': self.desc,
                    'ostypeid': self.ostype,
                }
                cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
                serializer = CollPolicyGroupSerializer(data=data)
                if serializer.is_valid(Exception):
                    serializer.save()
                    policy_group_data = []
                    for per_cp in cps:
                        per_cp['policy_group'] = int(serializer.data.get('policy_group_id'))
                        per_cp['history'] = time.time()
                        per_cp['policy'] = per_cp['collection_policy_id']
                        policy_group_data.append(per_cp)
                    serializer_related = PolicyGroupSerializer(data=policy_group_data, many=True)
                    if serializer_related.is_valid(Exception):
                        serializer_related.save()
                    data = {
                        'data_coll_policy': serializer.data,
                        'data_policys_groups': serializer_related.data,
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

    def put(self):
        try:
            cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
            kwargs = {'policy_group_id': self.id}
            detail = self.get_schedule(**kwargs)
            if detail is False:
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: 'Current Policy Group is exist in Schedule, so you can not modify it.'
                    }
                }
                return api_return(data=data)
            queryset = self.get_cp_group(**kwargs)
            if len(queryset) <= 0:
                if json.loads(queryset)['message'] is not '':
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: json.loads(queryset)['message']
                        }
                    }
                    return api_return(data=data)
            delete_return = self.del_policy_group(**kwargs)
            if delete_return is False:
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.FAILED
                    }
                }
                return api_return(data=data)
            data = {
                'name': self.name,
                'desc': self.desc,
                'ostypeid': self.ostype,
            }
            serializer = CollPolicyGroupSerializer(data=data)
            if serializer.is_valid(Exception):
                serializer.save()
                policy_group_data = []
                for per_cp in cps:
                    per_cp['policy_group'] = int(serializer.data.get('policy_group_id'))
                    per_cp['history'] = time.time()
                    per_cp['policy'] = per_cp['collection_policy_id']
                    policy_group_data.append(per_cp)
                serializer_related = PolicyGroupSerializer(data=policy_group_data, many=True)
                if serializer_related.is_valid(Exception):
                    serializer_related.save()
                data = {
                    'data_coll_policy': serializer.data,
                    'data_policys_groups': serializer_related.data,
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

    def delete(self):
        # http://127.0.0.1:1111/v1/api_collection_policy_group/?id=5
        try:
            kwargs = {'policy_group_id': self.id}
            detail = self.get_schedule(**kwargs)
            if detail is False:
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: 'Current Policy Group is exist in Schedule, so you can not delete it.'
                    }
                }
                return api_return(data=data)
            queryset = self.get_cp_group(**kwargs)
            if json.loads(queryset)['message'] is not '':
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: json.loads(queryset)['message']
                    }
                }
                return api_return(data=data)
            queryset.delete()
            delete_return = self.del_policy_group(**kwargs)
            if delete_return is False:
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.FAILED
                    }
                }
                return api_return(data=data)
            data = {
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
