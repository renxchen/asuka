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
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback
import time


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
            pg = self.get_policy_group(**kwargs)
            return pg.delete()
        except PolicysGroups.DoesNotExist:
            return False

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
                    'table_data': contacts.object_list,
                    'num_page': paginator.num_pages,
                    'page_range': list(paginator.page_range),
                    'page_has_next': contacts.has_next(),
                    'total_num': total_related_num,
                    'current_page_num': contacts.number,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS,
                        'data': serializer.data,
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
            data = {
                'name': self.name,
                'desc': self.desc,
                'ostypeid': self.ostype,
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
                        data = {
                            constants.MESSAGE: serializer_related.errors,
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.FAILED
                            }
                        }
                        return api_return(data=data)
                data = {
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
        try:
            cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
            kwargs = {'policy_group_id': self.id}
            queryset = self.get_cp_group(**kwargs)
            queryset_pg = self.get_policy_group(**kwargs)
            if queryset is False:
                message = 'There is no result for current query.'
                data = {
                    constants.MESSAGE: message,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.FAILED
                    }
                }
                return api_return(data=data)
            if queryset_pg is False:
                message = 'There is no result found in current policy group.'
                data = {
                    constants.MESSAGE: message,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.FAILED
                    }
                }
                return api_return(data=data)
            self.del_policy_group(**kwargs)
            data = {
                'name': self.name,
                'desc': self.desc,
                'ostype': self.ostype,
            }
            serializer = CollPolicyGroupSerializer(queryset, data=data)
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
                        data = {
                            constants.MESSAGE: serializer_related.errors,
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.FAILED
                            }
                        }
                        return api_return(data=data)
                data = {
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

    def delete(self):
        # http://127.0.0.1:1111/v1/api_collection_policy_group/?id=5
        try:
            kwargs = {'policy_group_id': self.id}
            queryset = self.get_cp_group(**kwargs)
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
