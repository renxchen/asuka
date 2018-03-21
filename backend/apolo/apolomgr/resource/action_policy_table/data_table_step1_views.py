#!/usr/bin/env python
# coding=utf-8
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
from backend.apolo.models import DataTable, DataTableItems, DataTableHistoryItems
from django.db import transaction
from backend.apolo.serializer.action_policy_serializer import ActionPolicyDataTableSerializer, \
    ActionPolicyDataTableItemSerializer
from backend.apolo.serializer.history_x_serializer import HistoryXSerializer
import time
import simplejson as json
from backend.apolo.apolomgr.resource.common import csv_export
import os


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
        self.coll_policy_group_id = views_helper.get_request_value(self.request, 'coll_policy_group_id', method)
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
        """!@brief
        Get the data of DataTable table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of DataTable table
        @post return DataTable data
        @return result: data of DataTable table
        """
        try:
            dt = DataTable.objects.filter(**kwargs)
            return dt
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_data_table_item(**kwargs):
        """!@brief
        Get the data of DataTableItems table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of DataTableItems table
        @post return DataTableItems data
        @return result: data of DataTableItems table
        """
        try:
            data_table_item_info = DataTableItems.objects.filter(**kwargs).values('item', 'item__value_type',
                                                                                  'item__item_type',
                                                                                  'item__device__hostname',
                                                                                  'item__coll_policy_rule_tree_treeid__rule__key_str')
            return data_table_item_info
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_data_table_history_item(**kwargs):
        """!@brief
        Get the data of DataTableItems table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of DataTableItems table
        @post return DataTableItems data
        @return result: data of DataTableItems table
        """
        try:
            data_table_history_item_info = DataTableHistoryItems.objects.filter(**kwargs).values('item',
                                                                                                 'item__value_type',
                                                                                                 'item__item_type',
                                                                                                 'item__device__hostname',
                                                                                                 'item__coll_policy_rule_tree_treeid__rule__key_str')
            return data_table_history_item_info
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_mapping(code):
        """!@brief
        Match the value type， change the integer value into string value,
        0: snmp, 1: cli, 2: float, 3: string, 4: text, 5: int
        @param code: the integer value of value type
        @pre call when need to change value type
        @post return the value type
        @return code_meaning: string value type
        """
        # value = Mapping.objects.filter(**{'code': code}).values('code_meaning')[0]
        code_meaning = ''
        if code == constants.NUMBER_ZERO:
            code_meaning = constants.SNMP
        if code == constants.NUMBER_ONE:
            code_meaning = constants.CLI
        if code == constants.NUMBER_TWO:
            code_meaning = constants.FLOAT
        if code == constants.NUMBER_THREE:
            code_meaning = constants.STRING
        if code == constants.NUMBER_FOUR:
            code_meaning = constants.TEXT
        if code == constants.NUMBER_FIVE:
            code_meaning = constants.INTEGER
        return code_meaning

    def get_history(self, item_id, value_type, policy_type):
        """!@brief
        Get history data from History%s%s table
        @param item_id: item id
        @param value_type: value type(str, int, float, text)
        @param policy_type: policy type(cli, snmp)
        @note
        @return history: history data(type is list)
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

    def get_info_by_table_id(self, id, history_need_flag=True):
        """!@brief
        Get the data when click [表示] button according the search by and sort by
        @param id: table id
        @param history_need_flag: if history_need_flag=True, will show the data from data_table_history_items table
        @node: history_need_flag exist for click [Column] button in 新规页面, if in that page no need history data, will not show the data from data_table_history_items table
        @return data: history data(type is list)
        """
        result = []
        result_temp = []
        result_history_temp = []
        data_history = {}
        # get all items by provided table id
        # data_table_item_info = self.get_data_table_item(**{'table_id': id, 'item__enable_status': 1})
        data_table_item_info = self.get_data_table_item(**{'table_id': id})
        data_table_history_item_info = self.get_data_table_history_item(**{'table_id': id})
        for per_data_table_item_info in data_table_item_info:
            # value type in item table
            value_type = self.get_mapping(per_data_table_item_info['item__value_type'])
            # item type in item table
            item_type = self.get_mapping(per_data_table_item_info['item__item_type'])
            # host name in Devices table
            hostname = per_data_table_item_info['item__device__hostname']
            # item id in item table
            item_id = per_data_table_item_info['item']
            table_id = id
            # key_str in rule table
            key_str = per_data_table_item_info['item__coll_policy_rule_tree_treeid__rule__key_str']
            history_data = self.get_history(per_data_table_item_info['item'], value_type, item_type)
            serializer = HistoryXSerializer(history_data, many=True)
            for per in serializer.data:
                per['item_id'] = item_id
                per['table_id'] = table_id
                per['device_name'] = hostname
                per['key_str'] = key_str
                result_temp.append(per)
        # get the data from data_table_history_items table for show the history data when device reloaded
        if history_need_flag:
            for per_data_table_history_item_info in data_table_history_item_info:
                # value type in item table
                value_type = self.get_mapping(per_data_table_history_item_info['item__value_type'])
                # item type in item table
                item_type = self.get_mapping(per_data_table_history_item_info['item__item_type'])
                # host name in Devices table
                hostname = per_data_table_history_item_info['item__device__hostname']
                # item id in item table
                item_id = per_data_table_history_item_info['item']
                table_id = id
                # key_str in rule table
                key_str = per_data_table_history_item_info['item__coll_policy_rule_tree_treeid__rule__key_str']
                history_data = self.get_history(per_data_table_history_item_info['item'], value_type, item_type)
                serializer = HistoryXSerializer(history_data, many=True)
                for per in serializer.data:
                    per['item_id'] = item_id
                    per['table_id'] = table_id
                    per['device_name'] = hostname
                    per['key_str'] = key_str
                    result_history_temp.append(per)
        # delete the repeating data from data_table_history_items and data_table_item
        result_history_without_repeating = []
        for per_history in result_history_temp:
            repeating_flag = False
            for per in result_temp:
                if per_history['item_id'] == per['item_id']:
                    repeating_flag = True
            if not repeating_flag:
                result_history_without_repeating.append(per_history)
        result_temp = result_temp + result_history_without_repeating
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
            'data': {
                'data': result
            },
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

    def csv_export(self):
        try:
            if self.id is not '':
                data = self.get_info_by_table_id(self.id)
                title = ['デバイス名', 'Time Stamp', 'Path', data['data']['data'][0]['checkitem']]
                csv_data = []
                for per in data['data']['data']:
                    csv_data.append([per['hostname'], per['date'], per['path'], per['value']])
                script_dir = os.path.split(os.path.realpath(__file__))[0]
                csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))),
                                        constants.CSV_PATH)
                csv_data.insert(0, title)
                # create csv
                result = csv_export.csv_export(csv_path, csv_data)
                # download csv
                if result is False:
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: result
                        },
                    }
                    return api_return(data=data)
                return result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def get(self):
        """!@brief
        Rest Api of GET, get all the data for summary page or get the data according to table id
        @return data: the data for summary page
        """
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
                queryset = DataTable.objects.filter(**search_conditions).values(
                    *['table_id', 'descr', 'name', 'coll_policy', 'groups', 'tree']).order_by(*sorts)
            else:
                queryset = DataTable.objects.all().values(
                    *['table_id', 'descr', 'name', 'coll_policy', 'groups', 'tree']).order_by(*sorts)
            # serializer = ActionPolicyDataTableSerializer(queryset, many=True)
            paginator = Paginator(list(queryset), int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': {
                    'data': contacts.object_list,
                },
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                # 'page_range': list(paginator.page_range),
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
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        """!@brief
        Rest Api of POST, create data table, Insert data into DataTable table, DataTableItems table
        @return data: the status of whether insert successful, and inserted data
        """
        try:
            with transaction.atomic():
                data = {
                    'name': self.name,
                    'descr': self.desc,
                    'coll_policy': self.coll_policy_id,
                    'policy_group': self.coll_policy_group_id,
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
                            'data': {
                                'data_table': serializer.data,
                                'data_table_item': serializer_data_table_item.data,
                            },
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
        """!@brief
        Rest Api of DELETE, delete data according to table id
        @return data: the status of whether delete successful
        """
        try:
            with transaction.atomic():
                kwargs = {'table_id': self.id}
                data_in_dp = self.get_data_table(**kwargs)
                if len(data_in_dp) <= 0:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.DATA_TABLE_NOT_EXIST_IN_SYSTEM
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
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
