#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: table_views.py
@time: 2018/1/3 17:25
@desc:

"""
import traceback
import importlib
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import DataTable, DataTableItems
from django.db import transaction
from backend.apolo.serializer.action_policy_serializer import ActionPolicyDataTableSerializer, \
    ActionPolicyDataTableItemSerializer
from backend.apolo.serializer.history_x_serializer import HistoryXSerializer
import time
import simplejson as json


class TableViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(TableViewsSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        method = 'GET'
        if request.method.lower() == 'get':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.name = views_helper.get_request_value(self.request, 'name', method)
        self.coll_policy_id = views_helper.get_request_value(self.request, 'coll_policy_id', method)
        self.tree_id = views_helper.get_request_value(self.request, 'tree_id', method)
        self.group_id = views_helper.get_request_value(self.request, 'group_id', method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        # table detail page sort parameters
        self.sort_by = views_helper.get_request_value(self.request, 'sidx', method)
        self.order = views_helper.get_request_value(self.request, 'sord', method)
        # table detail page search parameters
        self.hostname = views_helper.get_request_value(self.request, 'hostname', method)
        self.timestamp = views_helper.get_request_value(self.request, 'timestamp', method)
        self.path = views_helper.get_request_value(self.request, 'path', method)
        self.checkitem_value = views_helper.get_request_value(self.request, 'value', method)
        # table detail page search button parameters, start date and end date format 2016-06-06 16:16:16
        self.start_date = views_helper.get_request_value(self.request, 'start_date', method)
        self.end_date = views_helper.get_request_value(self.request, 'end_date', method)
        self.start_date_timestamp = 0
        self.end_date_timestamp = 0
        if self.start_date and self.end_date:
            self.start_date_timestamp = time.mktime(time.strptime(self.start_date, "%Y-%m-%d %H:%M:%S"))
            self.end_date_timestamp = time.mktime(time.strptime(self.end_date, "%Y-%m-%d %H:%M:%S"))
        self.item_ids = views_helper.get_request_value(self.request, 'item_id', method).split(',')

    @staticmethod
    def get_data_table(**kwargs):
        try:
            dt = DataTable.objects.filter(**kwargs)
            return dt
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_data_table_item(**kwargs):
        try:
            data_table_item_info = DataTableItems.objects.filter(**kwargs).values('item', 'item__value_type',
                                                                                  'item__item_type',
                                                                                  'item__device__hostname',
                                                                                  'item__coll_policy_rule_tree_treeid__rule__key_str')
            return data_table_item_info
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_mapping(code):
        """
        Search mapping relationship by given code
        :param code:
        :return: code meaning
        """
        # value = Mapping.objects.filter(**{'code': code}).values('code_meaning')[0]
        code_meaning = ''
        if code == 0:
            code_meaning = 'snmp'
        if code == 1:
            code_meaning = 'cli'
        if code == 2:
            code_meaning = 'float'
        if code == 3:
            code_meaning = 'string'
        if code == 4:
            code_meaning = 'text'
        if code == 5:
            code_meaning = 'int'
        return code_meaning

    def get_history(self, item_id, value_type, policy_type):
        """
        Search history data from db by given item id and value type
        :param item_id:
        :param policy_type:
        :param value_type:
        :return: history list
        """

        base_db_format = "History%s%s"
        trigger_db_modules = "backend.apolo.models"
        trigger_numeric = ["Float", "Int"]
        table_name = base_db_format % (policy_type.capitalize(), value_type.capitalize())
        db_module = importlib.import_module(trigger_db_modules)
        if hasattr(db_module, table_name) is False:
            raise Exception("%s table isn't exist" % table_name)
        table = getattr(db_module, table_name)
        kwargs = {
            "item_id": item_id,
        }
        if self.start_date and self.end_date:
            kwargs = {
                "item_id": item_id,
                'clock__gte': self.start_date_timestamp,
                'clock__lte': self.end_date_timestamp
            }
        history = table.objects.filter(**kwargs).order_by("-clock")
        if value_type not in trigger_numeric:
            for h in history:
                # h.value = "'" + h.value + "'"
                h.value = str(h.value)
        return history

    def get_info_by_table_id(self, id):
        result = []
        result_temp = []
        data_history = {}
        # get all items by provided table id
        data_table_item_info = self.get_data_table_item(**{'table_id': id})
        for per_data_table_item_info in data_table_item_info:
            # value type in item table
            value_type = self.get_mapping(per_data_table_item_info['item__value_type'])
            # item type in item table
            item_type = self.get_mapping(per_data_table_item_info['item__item_type'])
            # host name in Devices table
            hostname = per_data_table_item_info['item__device__hostname']
            # key_str in rule table
            key_str = per_data_table_item_info['item__coll_policy_rule_tree_treeid__rule__key_str']
            history_data = self.get_history(per_data_table_item_info['item'], value_type, item_type)
            serializer = HistoryXSerializer(history_data, many=True)
            for per in serializer.data:
                per['device_name'] = hostname
                per['key_str'] = key_str
                result_temp.append(per)
        paginator = Paginator(result_temp, int(self.max_size_per_page))
        contacts = paginator.page(int(self.page_from))
        for per_history_data in contacts.object_list:
            timestamp = per_history_data['clock']
            path = per_history_data['block_path']
            value = per_history_data['value']
            device_name = per_history_data['device_name']
            key_str = per_history_data['key_str']
            # table detail page search button start
            if self.hostname and self.hostname not in device_name:
                continue
            if self.timestamp and self.timestamp not in str(timestamp):
                continue
            if self.path and self.path not in path:
                continue
            if self.checkitem_value and self.checkitem_value not in str(value):
                continue
            # table detail page search button end
            data_history['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
            data_history['path'] = path
            data_history['value'] = value
            data_history['hostname'] = device_name
            data_history['checkitem'] = key_str
            result.append(data_history.copy())
        # table detail page sort start
        sort_by_list = ['hostname', 'date', 'path', 'value']
        if self.sort_by and self.sort_by in sort_by_list:
            if self.order:
                # True: asc, False: desc
                reverse = True
                if self.order.strip().lower() == 'asc'.strip().lower():
                    reverse = False
                result = sorted(result, key=lambda result: result[self.sort_by], reverse=reverse)
        # table detail page sort end
        data = {
            'data': result,
            'new_token': self.new_token,
            'num_page': paginator.num_pages,
            'page_range': list(paginator.page_range),
            'page_has_next': contacts.has_next(),
            'total_num': len(result_temp),
            'current_page_num': contacts.number,
            constants.STATUS: {
                constants.STATUS: constants.TRUE,
                constants.MESSAGE: constants.SUCCESS
            },
        }
        return data

    def get(self):
        try:
            if self.id is not '':
                data = self.get_info_by_table_id(self.id)
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
                    'coll_policy': self.coll_policy_id,
                    'tree': self.tree_id,
                    'groups': self.group_id,
                }
                if self.name is not '':
                    get_name_from_data_table = self.get_data_table(**{'name': self.name})
                    if len(get_name_from_data_table) > 0:
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
            transaction.rollback()
            print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        pass

    def delete(self):
        try:
            with transaction.atomic():
                kwargs = {'table_id': self.id}
                data_in_dp = self.get_data_table(**kwargs)
                if len(data_in_dp) <= 0:
                    if json.loads(data_in_dp)['message'] is not '':
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: json.loads(data_in_dp)['message']
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
            transaction.rollback()
            print traceback.format_exc(e)
            return exception_handler(e)
