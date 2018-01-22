#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: table_views.py
@time: 2018/1/3 17:25
@desc:

"""
import traceback

from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import DataTable
from django.db import transaction
from backend.apolo.serializer.action_policy_serializer import ActionPolicyDataTableSerializer, \
    ActionPolicyDataTableItemSerializer


class TableViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(TableViewsSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.name = views_helper.get_request_value(self.request, 'name', 'GET')
        self.desc = views_helper.get_request_value(self.request, 'desc', 'GET')
        self.item_ids = views_helper.get_request_value(self.request, 'item_id', 'GET').split(',')

    @staticmethod
    def get_data_table(**kwargs):
        try:
            return DataTable.objects.get(**kwargs)
        except DataTable.DoesNotExist:
            return False

    def get(self):
        try:
            if self.id is not '':
                queryset = DataTable.objects.filter(**{'table_id': self.id})
                serializer = ActionPolicyDataTableSerializer(queryset, many=True)
                data = {
                    'data': serializer.data,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                return api_return(data=data)
            field_relation_ships = {
                'table_id': 'id',
                'name': 'name',
                'descr': 'descr',
            }
            query_data = {
                'name': self.name,
                'desc': self.desc,
            }
            search_fields = ['name', 'desc']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            total_num = len(DataTable.objects.all())
            if search_conditions:
                queryset = DataTable.objects.filter(**search_conditions).order_by(*sorts)
            else:
                queryset = DataTable.objects.all().order_by(*sorts)
            serializer = ActionPolicyDataTableSerializer(queryset, many=True)
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
        try:
            with transaction.atomic():
                data = {
                    'name': self.name,
                    'descr': self.desc,
                }
                if self.name is not '':
                    get_name_from_data_table = self.get_data_table(**{'name': self.name})
                    if get_name_from_data_table is not False:
                        data = {
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.DATA_TABLE_NAME_DUPLICATE
                            }
                        }
                        return api_return(data=data)
                serializer = ActionPolicyDataTableSerializer(data=data)
                if serializer.is_valid(Exception):
                    serializer.save()
                    table_id = serializer.data['table_id']
                    data_table_item = []
                    for per_item_id in self.item_ids:
                        data_table_item.append({'item': per_item_id, 'table': table_id})
                    serializer_data_table_item = ActionPolicyDataTableItemSerializer(data=data_table_item, many=True)
                    if serializer_data_table_item.is_valid(Exception):
                        serializer_data_table_item.save()
                        data = {
                            'data_table': serializer.data,
                            'data_table_item': serializer_data_table_item.data,
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
        pass

    def delete(self):
        try:
            with transaction.atomic():
                kwargs = {'table_id': self.id}
                data_in_dp = self.get_data_table(**kwargs)
                if data_in_dp is False:
                    message = 'There is no result for current query.'
                    data = {
                        'data': message,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.FAILED
                        }
                    }
                    return api_return(data=data)
                data_in_dp.delete()
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
