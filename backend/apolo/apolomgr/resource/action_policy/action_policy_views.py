#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: kimli
@contact: kimli@cisco.com
@file: action_policy_views.py
@time: 2018/1/3 17:34
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
from backend.apolo.models import Triggers, TriggerDetail, DataTableItems, Actions, DataTable
from django.db import transaction
from backend.apolo.serializer.action_policy_serializer import TriggerSerializer, ActionsSerializer, \
    TriggerDetailSerializer
import logging
from django.db.models import *
import sys
from backend.apolo.apolomgr.resource.action_policy.mem_cache_trigger_and_trigger_detial import \
    MemCacheTriggerTriggerDetail
# from apolo_server.processor.db_units.memcached_helper import TriggerMemCache

reload(sys)
sys.setdefaultencoding('utf-8')


class ActionPolicyViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(ActionPolicyViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.logger = logging.getLogger("apolo.log")
        method = 'GET'
        if request.method.lower() == 'get' or request.method.lower() == 'delete':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.trigger_id = views_helper.get_request_value(self.request, 'trigger_id', method)
        self.table_id = views_helper.get_request_value(self.request, 'id', method)
        self.sort_by = views_helper.get_request_value(self.request, 'sidx', method)
        self.order = views_helper.get_request_value(self.request, 'sord', method)
        self.action_policy_name = views_helper.get_request_value(self.request, 'name', method)
        self.action_policy_name_get_put_delete = views_helper.get_request_value(self.request, 'name_get_put_delete',
                                                                                'GET')
        self.action_policy_name_for_search = views_helper.get_request_value(self.request, 'name_for_search', method)
        self.device_group_name_for_search = views_helper.get_request_value(self.request, 'device_group_name_for_search',
                                                                           method)
        self.coll_policy_group_name_for_search = views_helper.get_request_value(self.request,
                                                                                'coll_policy_group_name_for_search',
                                                                                method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        self.trigger_type = views_helper.get_request_value(self.request, 'trigger_type', method)
        self.column_a = views_helper.get_request_value(self.request, 'column_a', method)
        self.column_b = views_helper.get_request_value(self.request, 'column_b', method)
        # critical parameters start
        self.critical_priority = views_helper.get_request_value(self.request, 'critical_priority', method)
        self.critical_threshold = views_helper.get_request_value(self.request, 'critical_threshold', method)
        self.critical_condition = views_helper.get_request_value(self.request, 'critical_condition', method)
        self.critical_limit_nums = views_helper.get_request_value(self.request, 'critical_limit_nums', method)
        self.critical_action_type_1 = views_helper.get_request_value(self.request, 'critical_action_type_1', method)
        self.critical_action_type_2 = views_helper.get_request_value(self.request, 'critical_action_type_2', method)
        # critical action type is SNMP Trap
        # self.action_multi = views_helper.get_request_value(self.request, 'action_multi', method)
        # 1
        self.critical_snmp_version_1 = views_helper.get_request_value(self.request, 'critical_snmp_version_1', method)
        self.critical_snmp_comminute_1 = views_helper.get_request_value(self.request, 'critical_snmp_comminute_1',
                                                                        method)
        self.critical_agent_address_1 = views_helper.get_request_value(self.request, 'critical_agent_address_1', method)
        self.critical_destination_address_1 = views_helper.get_request_value(self.request,
                                                                             'critical_destination_address_1',
                                                                             method)
        self.critical_oid_1 = views_helper.get_request_value(self.request, 'critical_oid_1', method)
        self.critical_msg_1 = views_helper.get_request_value(self.request, 'critical_msg_1', method)
        self.critical_action_timing_1 = views_helper.get_request_value(self.request, 'critical_action_timing_1', method)
        # 2
        self.critical_snmp_version_2 = views_helper.get_request_value(self.request, 'critical_snmp_version_2', method)
        self.critical_snmp_comminute_2 = views_helper.get_request_value(self.request, 'critical_snmp_comminute_2',
                                                                        method)
        self.critical_agent_address_2 = views_helper.get_request_value(self.request, 'critical_agent_address_2', method)
        self.critical_destination_address_2 = views_helper.get_request_value(self.request,
                                                                             'critical_destination_address_2',
                                                                             method)
        self.critical_oid_2 = views_helper.get_request_value(self.request, 'critical_oid_2', method)
        self.critical_msg_2 = views_helper.get_request_value(self.request, 'critical_msg_2', method)
        self.critical_action_timing_2 = views_helper.get_request_value(self.request, 'critical_action_timing_2', method)
        # critical action type is script execute
        # 1
        self.critical_execute_script_1 = views_helper.get_request_value(self.request, 'critical_execute_script_1',
                                                                        method)
        # 2
        self.critical_execute_script_2 = views_helper.get_request_value(self.request, 'critical_execute_script_2',
                                                                        method)
        # critical action type is runner execute
        # 1
        self.critical_runner_server_1 = views_helper.get_request_value(self.request, 'critical_runner_server_1', method)
        self.critical_runner_username_1 = views_helper.get_request_value(self.request, 'critical_runner_username_1',
                                                                         method)
        self.critical_runner_password_1 = views_helper.get_request_value(self.request, 'critical_runner_password_1',
                                                                         method)
        self.critical_runner_command_1 = views_helper.get_request_value(self.request, 'critical_runner_command_1',
                                                                        method)
        # 2
        self.critical_runner_server_2 = views_helper.get_request_value(self.request, 'critical_runner_server_2', method)
        self.critical_runner_username_2 = views_helper.get_request_value(self.request, 'critical_runner_username_2',
                                                                         method)
        self.critical_runner_password_2 = views_helper.get_request_value(self.request, 'critical_runner_password_2',
                                                                         method)
        self.critical_runner_command_2 = views_helper.get_request_value(self.request, 'critical_runner_command_2',
                                                                        method)
        # critical parameters end
        # minor parameters start
        self.minor_priority = views_helper.get_request_value(self.request, 'minor_priority', method)
        self.minor_threshold = views_helper.get_request_value(self.request, 'minor_threshold', method)
        self.minor_condition = views_helper.get_request_value(self.request, 'minor_condition', method)
        self.minor_limit_nums = views_helper.get_request_value(self.request, 'minor_limit_nums', method)
        self.minor_action_type_1 = views_helper.get_request_value(self.request, 'minor_action_type_1', method)
        self.minor_action_type_2 = views_helper.get_request_value(self.request, 'minor_action_type_2', method)
        # minor action type is SNMP Trap
        # 1
        self.minor_snmp_version_1 = views_helper.get_request_value(self.request, 'minor_snmp_version_1', method)
        self.minor_snmp_comminute_1 = views_helper.get_request_value(self.request, 'minor_snmp_comminute_1',
                                                                     method)
        self.minor_agent_address_1 = views_helper.get_request_value(self.request, 'minor_agent_address_1', method)
        self.minor_destination_address_1 = views_helper.get_request_value(self.request,
                                                                          'minor_destination_address_1',
                                                                          method)
        self.minor_oid_1 = views_helper.get_request_value(self.request, 'minor_oid_1', method)
        self.minor_msg_1 = views_helper.get_request_value(self.request, 'minor_msg_1', method)
        self.minor_action_timing_1 = views_helper.get_request_value(self.request, 'minor_action_timing_1', method)
        # 2
        self.minor_snmp_version_2 = views_helper.get_request_value(self.request, 'minor_snmp_version_2', method)
        self.minor_snmp_comminute_2 = views_helper.get_request_value(self.request, 'minor_snmp_comminute_2',
                                                                     method)
        self.minor_agent_address_2 = views_helper.get_request_value(self.request, 'minor_agent_address_2', method)
        self.minor_destination_address_2 = views_helper.get_request_value(self.request,
                                                                          'minor_destination_address_2',
                                                                          method)
        self.minor_oid_2 = views_helper.get_request_value(self.request, 'minor_oid_2', method)
        self.minor_msg_2 = views_helper.get_request_value(self.request, 'minor_msg_2', method)
        self.minor_action_timing_2 = views_helper.get_request_value(self.request, 'minor_action_timing_2', method)
        # minor action type is script execute
        # 1
        self.minor_execute_script_1 = views_helper.get_request_value(self.request, 'minor_execute_script_1',
                                                                     method)
        # 2
        self.minor_execute_script_2 = views_helper.get_request_value(self.request, 'minor_execute_script_2',
                                                                     method)
        # minor action type is runner execute
        # 1
        self.minor_runner_server_1 = views_helper.get_request_value(self.request, 'minor_runner_server_1', method)
        self.minor_runner_username_1 = views_helper.get_request_value(self.request, 'minor_runner_username_1',
                                                                      method)
        self.minor_runner_password_1 = views_helper.get_request_value(self.request, 'minor_runner_password_1',
                                                                      method)
        self.minor_runner_command_1 = views_helper.get_request_value(self.request, 'minor_runner_command_1',
                                                                     method)
        # 2
        self.minor_runner_server_2 = views_helper.get_request_value(self.request, 'minor_runner_server_2', method)
        self.minor_runner_username_2 = views_helper.get_request_value(self.request, 'minor_runner_username_2',
                                                                      method)
        self.minor_runner_password_2 = views_helper.get_request_value(self.request, 'minor_runner_password_2',
                                                                      method)
        self.minor_runner_command_2 = views_helper.get_request_value(self.request, 'minor_runner_command_2',
                                                                     method)
        # minor parameters end
        # major parameters start
        self.major_priority = views_helper.get_request_value(self.request, 'major_priority', method)
        self.major_threshold = views_helper.get_request_value(self.request, 'major_threshold', method)
        self.major_condition = views_helper.get_request_value(self.request, 'major_condition', method)
        self.major_limit_nums = views_helper.get_request_value(self.request, 'major_limit_nums', method)
        self.major_action_type_1 = views_helper.get_request_value(self.request, 'major_action_type_1', method)
        self.major_action_type_2 = views_helper.get_request_value(self.request, 'major_action_type_2', method)
        # major action type is SNMP Trap
        # 1
        self.major_snmp_version_1 = views_helper.get_request_value(self.request, 'major_snmp_version_1', method)
        self.major_snmp_comminute_1 = views_helper.get_request_value(self.request, 'major_snmp_comminute_1',
                                                                     method)
        self.major_agent_address_1 = views_helper.get_request_value(self.request, 'major_agent_address_1', method)
        self.major_destination_address_1 = views_helper.get_request_value(self.request,
                                                                          'major_destination_address_1',
                                                                          method)
        self.major_oid_1 = views_helper.get_request_value(self.request, 'major_oid_1', method)
        self.major_msg_1 = views_helper.get_request_value(self.request, 'major_msg_1', method)
        self.major_action_timing_1 = views_helper.get_request_value(self.request, 'major_action_timing_1', method)
        # 2
        self.major_snmp_version_2 = views_helper.get_request_value(self.request, 'major_snmp_version_2', method)
        self.major_snmp_comminute_2 = views_helper.get_request_value(self.request, 'major_snmp_comminute_2',
                                                                     method)
        self.major_agent_address_2 = views_helper.get_request_value(self.request, 'major_agent_address_2', method)
        self.major_destination_address_2 = views_helper.get_request_value(self.request,
                                                                          'major_destination_address_2',
                                                                          method)
        self.major_oid_2 = views_helper.get_request_value(self.request, 'major_oid_2', method)
        self.major_msg_2 = views_helper.get_request_value(self.request, 'major_msg_2', method)
        self.major_action_timing_2 = views_helper.get_request_value(self.request, 'major_action_timing_2', method)
        # major action type is script execute
        # 1
        self.major_execute_script_1 = views_helper.get_request_value(self.request, 'major_execute_script_1',
                                                                     method)
        # 2
        self.major_execute_script_2 = views_helper.get_request_value(self.request, 'major_execute_script_2',
                                                                     method)
        # major action type is runner execute
        # 1
        self.major_runner_server_1 = views_helper.get_request_value(self.request, 'major_runner_server_1', method)
        self.major_runner_username_1 = views_helper.get_request_value(self.request, 'major_runner_username_1',
                                                                      method)
        self.major_runner_password_1 = views_helper.get_request_value(self.request, 'major_runner_password_1',
                                                                      method)
        self.major_runner_command_1 = views_helper.get_request_value(self.request, 'major_runner_command_1',
                                                                     method)
        # 2
        self.major_runner_server_2 = views_helper.get_request_value(self.request, 'major_runner_server_2', method)
        self.major_runner_username_2 = views_helper.get_request_value(self.request, 'major_runner_username_2',
                                                                      method)
        self.major_runner_password_2 = views_helper.get_request_value(self.request, 'major_runner_password_2',
                                                                      method)
        self.major_runner_command_2 = views_helper.get_request_value(self.request, 'major_runner_command_2',
                                                                     method)
        # major parameters end
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            if self.column_a is not '':
                self.expression = self.create_expression(self.trigger_type, self.column_a, self.column_b)
                self.expression_detail_result = self.tableid_change_to_itemid(self.column_a, self.column_b)

    @staticmethod
    def map_condition(value):
        """!@brief
        Match the condition expression， change the integer value into string value,
        0: <=, 1: ==, 2: >=, 3: !=, 4: <, 5: >
        @param value: the integer value of condition expression
        @pre call when need to change condition expression
        @post return the string condition
        @return condition_exp: string condition
        """
        condition_exp = ''
        if value == constants.NUMBER_ZERO:
            condition_exp = constants.LESS_THAN_OR_EQUAL_SIGN
        if value == constants.NUMBER_ONE:
            condition_exp = constants.EQUAL_SIGN
        if value == constants.NUMBER_TWO:
            condition_exp = constants.GREATER_THAN_OR_EQUAL_SIGN
        if value == constants.NUMBER_THREE:
            condition_exp = constants.NOT_EQUAL_SIGN
        if value == constants.NUMBER_FOUR:
            condition_exp = constants.LESS_THAN_SIGN
        if value == constants.NUMBER_FIVE:
            condition_exp = constants.GREATER_THAN_SIGN
        return condition_exp

    @staticmethod
    def map_priority(value):
        """!@brief
        Match the priority， change the integer value into string value,
        0: critical, 1: major, 2: minor
        @param value: the integer value of priority
        @pre call when need to change priority
        @post return string priority
        @return priority: string priority
        """
        priority = ''
        if value == constants.NUMBER_ZERO:
            priority = constants.PRIORITY_CRITICAL
        if value == constants.NUMBER_ONE:
            priority = constants.PRIORITY_MAJOR
        if value == constants.NUMBER_TWO:
            priority = constants.PRIORITY_MINOR
        return priority

    @staticmethod
    def map_trigger_type(value):
        """!@brief
        Match the trigger type， change the integer value into string value,
        0:演算比較,1:数値比較,2:文字列比較,3:取得失敗
        @param value: the integer value of trigger type
        @pre call when need to change trigger type
        @post return string trigger type
        @return trigger_type: string trigger type
        """
        trigger_type = ''
        if value == constants.NUMBER_ZERO:
            trigger_type = str(constants.TRIGGER_TYPE_EXPRESSION_COMPARE)
        if value == constants.NUMBER_ONE:
            trigger_type = str(constants.TRIGGER_TYPE_INTEGER_COMPARE)
        if value == constants.NUMBER_TWO:
            trigger_type = str(constants.TRIGGER_TYPE_STRING__COMPARE)
        if value == constants.NUMBER_THREE:
            trigger_type = str(constants.TRIGGER_TYPE_FAILED)
        return trigger_type

    @staticmethod
    def get_action_policy_in_trigger(**kwargs):
        """!@brief
        Get the data of Triggers table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of Triggers table
        @post return trigger data
        @return result: data of Triggers table
        """
        try:
            result = Triggers.objects.filter(**kwargs)
            return result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_data_table_items(**kwargs):
        """!@brief
        Get the queryset of the DataTableItems table
        @param kwargs: dictionary type of the query condition
        @pre call when need to select DataTableItems table
        @post according to the need to deal with the DataTableItems table
        @note
        @return result: queryset of DataTableItems table
        """
        try:
            result = DataTableItems.objects.filter(**kwargs).values('data_table_items_id', 'table_id', 'item_id',
                                                                    'item__device__device_id')
            return result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def delete_trigger_related(name):
        """!@brief
        Delete Actions table, TriggerDetail table and Triggers table according to name
        @param name: action name or trigger name
        @pre call when click delete button or modify button
        @post delete Actions table, TriggerDetail table and Triggers table according to name
        @return
        """
        try:
            with transaction.atomic():
                # delete action by action name
                Actions.objects.filter(action_name=name).delete()
                # select trigger_id by name
                trigger = Triggers.objects.filter(name=name)
                trigger_ids = trigger.values_list('trigger_id', flat=True)
                # delete trigger_detail by trigger_id
                for per_trigger_id in trigger_ids:
                    TriggerDetail.objects.filter(trigger_id=per_trigger_id).delete()
                trigger.delete()
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def migrate(data):
        temp = []
        for i in data:
            temp.append(i['action_type'])
        return ','.join(temp)

    def create_expression(self, value, column_a=None, column_b=None):
        """!@brief
        Generate expression according to the table id
        Change the column1(A) or column2(B) into corresponding table id, and return the 3 priorities of expression
        @param value: trigger type
        @param column_a: table id1
        @param column_b: table id2
        @pre call when need expression
        @post return the 3 priorities of expression
        @return expression: 3 priorities of expression (include of critical expression, major expression, minor expression)
        """
        expression = {}
        expression_critical = None
        expression_major = None
        expression_minor = None
        # 0:演算比較
        if value == constants.NUMBER_ZERO:
            # Min(A/B[10]) != 1500
            # A/B(10) > 1500 , 有括号的情况10表示倒数第10次
            # Hex2Dec(Min(A/B[10])) > 1500
            # Avg(A/B[10]) + Max(A/B[9]) > 1500
            # 4:table_id, 10:最近的十次， 9:最近的9次
            if self.critical_threshold is not '':
                expression_critical = self.critical_threshold.replace('A(', str(column_a) + '(').replace('A[', str(
                    column_a) + '[').replace('B(', str(column_b) + '(').replace('B[', str(column_b) + '[')
            if self.major_threshold is not '':
                expression_major = self.major_threshold.replace('A(', str(column_a) + '(').replace('A[', str(
                    column_a) + '[').replace('B(', str(column_b) + '(').replace('B[', str(column_b) + '[')
            if self.minor_threshold is not '':
                expression_minor = self.minor_threshold.replace('A(', str(column_a) + '(').replace('A[', str(
                    column_a) + '[').replace('B(', str(column_b) + '(').replace('B[', str(column_b) + '[')
        # 1:数値比較-->{4} == 'ok', 2:文字列比較-->{4} > 1000
        elif value == constants.NUMBER_ONE or value == constants.NUMBER_TWO:
            if self.critical_threshold is not '':
                expression_critical = '{' + str(column_a) + '}' + self.map_condition(self.critical_condition) + str(
                    self.critical_threshold)
            if self.major_threshold is not '':
                expression_major = '{' + str(column_a) + '}' + self.map_condition(self.major_condition) + str(
                    self.major_threshold)
            if self.minor_threshold is not '':
                expression_minor = '{' + str(column_a) + '}' + self.map_condition(self.minor_condition) + str(
                    self.minor_threshold)
        # 3:取得失敗-->Fail(1)
        elif value == constants.NUMBER_THREE:
            if self.critical_threshold is not '':
                expression_critical = 'Fail(' + str(column_a) + ')'
            if self.major_threshold is not '':
                expression_major = 'Fail(' + str(column_a) + ')'
            if self.minor_threshold is not '':
                expression_minor = 'Fail(' + str(column_a) + ')'
        expression['expression_critical'] = expression_critical
        expression['expression_major'] = expression_major
        expression['expression_minor'] = expression_minor

        return expression

    def tableid_change_to_itemid(self, column_a, column_b):
        """!@brief
        Generate expression for trigger_detail table,
        Change the column1(A) or column2(B) into corresponding item id with the same device, and return the expression
        @param column_a: table id1
        @param column_b: table id2
        @pre call when need to change table id to item id
        @post return expression with item id
        @note the result of the method will save into trigger_detial table for parse
        @return expression: dictionary of expression(include of critical expression, major expression, minor expression)
        """
        critical_detail_list = []
        major_detail_list = []
        minor_detail_list = []
        expression_detail_result = {
            'critical': None,
            'major': None,
            'minor': None
        }
        kwargs_a = {'table_id': column_a, 'item__enable_status': 1}
        kwargs_b = {'table_id': column_b, 'item__enable_status': 1}
        column_a_result = self.get_data_table_items(**kwargs_a)
        column_b_result = self.get_data_table_items(**kwargs_b)
        if len(column_a_result) > constants.NUMBER_ZERO:
            if column_a is not None and column_b is not None:
                for per_column_a in column_a_result:
                    device_id_a = per_column_a['item__device__device_id']
                    for per_column_b in column_b_result:
                        device_id_b = per_column_b['item__device__device_id']
                        if int(device_id_a) == int(device_id_b):
                            item_id_a = per_column_a['item_id']
                            item_id_b = per_column_b['item_id']
                            # self.column_a = item_id_a
                            # self.column_b = item_id_b
                            expression_detail = self.create_expression(self.trigger_type, item_id_a, item_id_b)
                            critical_detail = expression_detail['expression_critical']
                            major_detail = expression_detail['expression_major']
                            minor_detail = expression_detail['expression_minor']
                            critical_detail_list.append(critical_detail)
                            major_detail_list.append(major_detail)
                            minor_detail_list.append(minor_detail)
                            expression_detail_result['critical'] = critical_detail_list
                            expression_detail_result['major'] = major_detail_list
                            expression_detail_result['minor'] = minor_detail_list
            elif column_a is not None:
                for per_column_a in column_a_result:
                    item_id_a = per_column_a['item_id']
                    # self.column_a = item_id_a
                    expression_detail = self.create_expression(self.trigger_type, item_id_a)
                    critical_detail = expression_detail['expression_critical']
                    major_detail = expression_detail['expression_major']
                    minor_detail = expression_detail['expression_minor']
                    if self.trigger_type == constants.NUMBER_ONE or self.trigger_type == constants.NUMBER_TWO or self.trigger_type == constants.NUMBER_THREE:
                        critical_detail_list.append(critical_detail)
                        major_detail_list.append(major_detail)
                        minor_detail_list.append(minor_detail)
                    else:
                        critical_detail_list.append(critical_detail)
                        major_detail_list.append(major_detail)
                        minor_detail_list.append(minor_detail)

                    expression_detail_result['critical'] = critical_detail_list
                    expression_detail_result['major'] = major_detail_list
                    expression_detail_result['minor'] = minor_detail_list
        else:
            return False
        return expression_detail_result

    def regenerate_trigger_detail(self):
        """!@brief
        According to the Triggers table to regenerate trigger_detail table for re-upload device, the method will
        regenerate all data in trigger_detail table according to the Triggers.
        @pre call when the device was re-uploaded
        @post update trigger_detail table
        @note
        @return
        """
        try:
            with transaction.atomic():
                trigger_data = Triggers.objects.all()
                data = []
                trigger_detail_data = []
                for per in trigger_data:
                    self.critical_threshold = ''
                    self.major_threshold = ''
                    self.minor_threshold = ''
                    self.trigger_type = per.trigger_type
                    if per.priority == constants.NUMBER_ZERO:
                        self.critical_threshold = per.value
                        self.critical_condition = per.condition
                        critical_dic = self.tableid_change_to_itemid(per.columnA, per.columnB)
                        if critical_dic is False:
                            continue
                        data_trigger_detail = {
                            'trigger': per.trigger_id,
                            'expression': critical_dic['critical'],
                            'priority': per.priority,
                            'status': 1,
                            'expression_view': per.expression,
                        }
                        data.append(data_trigger_detail)
                    if per.priority == constants.NUMBER_ONE:
                        self.major_threshold = per.value
                        self.major_condition = per.condition
                        major_dic = self.tableid_change_to_itemid(per.columnA, per.columnB)
                        if major_dic is False:
                            continue
                        data_trigger_detail = {
                            'trigger': per.trigger_id,
                            'expression': major_dic['major'],
                            'priority': per.priority,
                            'status': 1,
                            'expression_view': per.expression,
                        }
                        data.append(data_trigger_detail)
                    if per.priority == constants.NUMBER_TWO:
                        self.minor_threshold = per.value
                        self.minor_condition = per.condition
                        minor_dic = self.tableid_change_to_itemid(per.columnA, per.columnB)
                        if minor_dic is False:
                            continue
                        data_trigger_detail = {
                            'trigger': per.trigger_id,
                            'expression': minor_dic['minor'],
                            'priority': per.priority,
                            'status': 1,
                            'expression_view': per.expression,
                        }
                        data.append(data_trigger_detail)
                TriggerDetail.objects.all().delete()
                for per in data:
                    expression_in_trigger_detail = per['expression']
                    for per_expression in expression_in_trigger_detail:
                        per_trigger_detail_data = {
                            'expression': per_expression,
                            'status': per['status'],
                            'trigger': per['trigger'],
                            'expression_view': per['expression_view']
                        }
                        trigger_detail_data.append(per_trigger_detail_data)
                serializer_trigger_detail = TriggerDetailSerializer(data=trigger_detail_data, many=True)
                if serializer_trigger_detail.is_valid(Exception):
                    serializer_trigger_detail.save()
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def data_generate_critical(self):
        """!@brief
        Generate critical data
        @pre call when need critical data
        @post return critical data
        @return result: dictionary of critical data
        """
        # create trigger from table page
        data_common = {
            'name': self.action_policy_name,  # アクションポリ シー名
            'descr': self.desc,  # 概要
            'trigger_type': self.trigger_type,  # 閾値タイプ
            'columnA': self.column_a,  # カラムA
            'columnB': self.column_b,  # カラムA
        }
        data_trigger = {
            'status': 1,  # 默认1
            'value': self.critical_threshold,  # 閾値
            'priority': self.critical_priority,  # 重要度
            'trigger_limit_nums': self.critical_limit_nums,  # 連続超過条件
            'condition': self.critical_condition,  # 条件 > < =
            'expression': self.expression['expression_critical'],  # table_id(value) 条件 value
        }
        data_trigger_detail = {
            'expression': self.expression_detail_result['critical'],
            'priority': self.critical_priority,  # 重要度
            # select data_table_items where table_id=table_id, each_item_id(value) 条件 value
            'status': 1,  # 默认1
            # 'trigger': 1,  # 当前的taigger_id
            'expression_view': self.expression['expression_critical'],  # 存tableid，table_id(10)
        }
        data_action_1 = {
            'action_name': self.action_policy_name,
            'action_type': self.critical_action_type_1,  # アクションタイプ
            'param': '',  #
            'priority': self.critical_priority,  # 重要度
            'snmp_version': self.critical_snmp_version_1,  # SNMP Version
            'snmp_oid': self.critical_oid_1,  # OID
            'community': self.critical_snmp_comminute_1,  # Community名
            'ip_address': self.critical_destination_address_1,
            # 宛先IPアドレス, ランナーサーバ (Rundeck) IP Address==self.critical_runner_server,
            'username': self.critical_runner_username_1,  # ランナー ユーザ名
            'password': self.critical_runner_password_1,  # ランナー パスワード
            'command': self.critical_runner_command_1,  # RUN COMMAND
            'agent_address': self.critical_agent_address_1,  # Agent Address(V1のみ)
            'oid': self.critical_oid_1,  # OID
            'message': self.critical_msg_1,  # メッセージ
            'script_path': self.critical_execute_script_1,  # 実行スクリプト
            'status': 1,  # 默认1
            'trigger': 1,  # 当前trigger_id
        }
        data_action_2 = {
            'action_name': self.action_policy_name,
            'action_type': self.critical_action_type_2,  # アクションタイプ
            'param': '',  #
            'priority': self.critical_priority,  # 重要度
            'snmp_version': self.critical_snmp_version_2,  # SNMP Version
            'snmp_oid': self.critical_oid_2,  # OID
            'community': self.critical_snmp_comminute_2,  # Community名
            'ip_address': self.critical_destination_address_2,
            # 宛先IPアドレス, ランナーサーバ (Rundeck) IP Address==self.critical_runner_server,
            'username': self.critical_runner_username_2,  # ランナー ユーザ名
            'password': self.critical_runner_password_2,  # ランナー パスワード
            'command': self.critical_runner_command_2,  # RUN COMMAND
            'agent_address': self.critical_agent_address_2,  # Agent Address(V1のみ)
            'oid': self.critical_oid_2,  # OID
            'message': self.critical_msg_2,  # メッセージ
            'script_path': self.critical_execute_script_2,  # 実行スクリプト
            'status': 1,  # 默认1
            'trigger': 1,  # 当前trigger_id
        }
        trigger_data = {}
        trigger_detail_data = {}
        action_data = []
        if self.critical_priority is not '':
            trigger_data = dict(data_common.items() + data_trigger.items())
            trigger_detail_data = data_trigger_detail
            if self.critical_action_type_1 is not '' and self.critical_action_type_2 is not '':
                action_data = [data_action_1, data_action_2]
            elif self.critical_action_type_1 is not '':
                action_data = [data_action_1]
            elif self.critical_action_type_2 is not '':
                action_data = [data_action_2]
        result = {
            'data_trigger': trigger_data,
            'trigger_detail_data': trigger_detail_data,
            'action_data': action_data,
        }
        return result

    def data_generate_major(self):
        """!@brief
        Generate major data
        @pre call when need major data
        @post return major data
        @return result: dictionary of major data
        """
        # create trigger from table page
        data_common = {
            'name': self.action_policy_name,  # アクションポリ シー名
            'descr': self.desc,  # 概要
            'trigger_type': self.trigger_type,  # 閾値タイプ
            'columnA': self.column_a,  # カラムA
            'columnB': self.column_b,  # カラムA
        }

        data_trigger = {
            'status': 1,  # 默认1
            'value': self.major_threshold,  # 閾値
            'priority': self.major_priority,  # 重要度
            'trigger_limit_nums': self.major_limit_nums,  # 連続超過条件
            'condition': self.major_condition,  # 条件 > < =
            'expression': self.expression['expression_major'],  # table_id(value) 条件 value
        }
        data_trigger_detail = {
            'expression': self.expression_detail_result['major'],
            'priority': self.major_priority,  # 重要度
            # select data_table_items where table_id=table_id, each_item_id(value) 条件 value
            'status': 1,  # 默认1
            # 'trigger': 1,  # 当前的taigger_id
            'expression_view': self.expression['expression_major'],  # ？？什么意思
        }
        data_action_1 = {
            'action_name': self.action_policy_name,
            'action_type': self.major_action_type_1,  # アクションタイプ
            'param': '',  #
            'priority': self.major_priority,  # 重要度
            'snmp_version': self.major_snmp_version_1,  # SNMP Version
            'snmp_oid': self.major_oid_1,  # OID
            'community': self.major_snmp_comminute_1,  # Community名
            'ip_address': self.major_destination_address_1,
            # 宛先IPアドレス, ランナーサーバ (Rundeck) IP Address==self.major_runner_server,
            'username': self.major_runner_username_1,  # ランナー ユーザ名
            'password': self.major_runner_password_1,  # ランナー パスワード
            'command': self.major_runner_command_1,  # RUN COMMAND
            'agent_address': self.major_agent_address_1,  # Agent Address(V1のみ)
            'oid': self.major_oid_1,  # OID
            'message': self.major_msg_1,  # メッセージ
            'script_path': self.major_execute_script_1,  # 実行スクリプト
            'status': 1,  # 默认1
            'trigger': 1,  # 当前trigger_id
        }

        data_action_2 = {
            'action_name': self.action_policy_name,
            'action_type': self.major_action_type_2,  # アクションタイプ
            'param': '',  #
            'priority': self.major_priority,  # 重要度
            'snmp_version': self.major_snmp_version_2,  # SNMP Version
            'snmp_oid': self.major_oid_2,  # OID
            'community': self.major_snmp_comminute_2,  # Community名
            'ip_address': self.major_destination_address_2,
            # 宛先IPアドレス, ランナーサーバ (Rundeck) IP Address==self.major_runner_server,
            'username': self.major_runner_username_2,  # ランナー ユーザ名
            'password': self.major_runner_password_2,  # ランナー パスワード
            'command': self.major_runner_command_2,  # RUN COMMAND
            'agent_address': self.major_agent_address_2,  # Agent Address(V1のみ)
            'oid': self.major_oid_2,  # OID
            'message': self.major_msg_2,  # メッセージ
            'script_path': self.major_execute_script_2,  # 実行スクリプト
            'status': 1,  # 默认1
            'trigger': 1,  # 当前trigger_id
        }

        trigger_data = {}
        trigger_detail_data = {}
        action_data = []
        if self.major_priority is not '':
            trigger_data = dict(data_common.items() + data_trigger.items())
            trigger_detail_data = data_trigger_detail
            if self.major_action_type_1 is not '' and self.major_action_type_2 is not '':
                action_data = [data_action_1, data_action_2]
            elif self.major_action_type_1 is not '':
                action_data = [data_action_1]
            elif self.major_action_type_2 is not '':
                action_data = [data_action_2]
        result = {
            'data_trigger': trigger_data,
            'trigger_detail_data': trigger_detail_data,
            'action_data': action_data,
        }
        return result

    def data_generate_minor(self):
        """!@brief
        Generate minor data
        @pre call when need minor data
        @post return minor data
        @return result: dictionary of minor data
        """
        # create trigger from table page
        data_common = {
            'name': self.action_policy_name,  # アクションポリ シー名
            'descr': self.desc,  # 概要
            'trigger_type': self.trigger_type,  # 閾値タイプ
            'columnA': self.column_a,  # カラムA
            'columnB': self.column_b,  # カラムA
        }
        data_trigger = {
            'status': 1,  # 默认1
            'value': self.minor_threshold,  # 閾値
            'priority': self.minor_priority,  # 重要度
            'trigger_limit_nums': self.minor_limit_nums,  # 連続超過条件
            'condition': self.minor_condition,  # 条件 > < =
            'expression': self.expression['expression_minor'],  # table_id(value) 条件 value
        }
        data_trigger_detail = {
            'expression': self.expression_detail_result['minor'],
            'priority': self.minor_priority,  # 重要度
            # select data_table_items where table_id=table_id, each_item_id(value) 条件 value
            'status': 1,  # 默认1
            # 'trigger': 1,  # 当前的taigger_id
            'expression_view': self.expression['expression_minor'],  # ？？什么意思
        }
        data_action_1 = {
            'action_name': self.action_policy_name,
            'action_type': self.minor_action_type_1,  # アクションタイプ
            'param': '',  #
            'priority': self.minor_priority,  # 重要度
            'snmp_version': self.minor_snmp_version_1,  # SNMP Version
            'snmp_oid': self.minor_oid_1,  # OID
            'community': self.minor_snmp_comminute_1,  # Community名
            'ip_address': self.minor_destination_address_1,
            # 宛先IPアドレス, ランナーサーバ (Rundeck) IP Address==self.minor_runner_server,
            'username': self.minor_runner_username_1,  # ランナー ユーザ名
            'password': self.minor_runner_password_1,  # ランナー パスワード
            'command': self.minor_runner_command_1,  # RUN COMMAND
            'agent_address': self.minor_agent_address_1,  # Agent Address(V1のみ)
            'oid': self.minor_oid_1,  # OID
            'message': self.minor_msg_1,  # メッセージ
            'script_path': self.minor_execute_script_1,  # 実行スクリプト
            'status': 1,  # 默认1
            'trigger': 1,  # 当前trigger_id
        }
        data_action_2 = {
            'action_name': self.action_policy_name,
            'action_type': self.minor_action_type_2,  # アクションタイプ
            'param': '',  #
            'priority': self.minor_priority,  # 重要度
            'snmp_version': self.minor_snmp_version_2,  # SNMP Version
            'snmp_oid': self.minor_oid_2,  # OID
            'community': self.minor_snmp_comminute_2,  # Community名
            'ip_address': self.minor_destination_address_2,
            # 宛先IPアドレス, ランナーサーバ (Rundeck) IP Address==self.minor_runner_server,
            'username': self.minor_runner_username_2,  # ランナー ユーザ名
            'password': self.minor_runner_password_2,  # ランナー パスワード
            'command': self.minor_runner_command_2,  # RUN COMMAND
            'agent_address': self.minor_agent_address_2,  # Agent Address(V1のみ)
            'oid': self.minor_oid_2,  # OID
            'message': self.minor_msg_2,  # メッセージ
            'script_path': self.minor_execute_script_2,  # 実行スクリプト
            'status': 1,  # 默认1
            'trigger': 1,  # 当前trigger_id
        }

        trigger_data = {}
        trigger_detail_data = {}
        action_data = []
        if self.minor_priority is not '':
            trigger_data = dict(data_common.items() + data_trigger.items())
            trigger_detail_data = data_trigger_detail
            if self.minor_action_type_1 is not '' and self.minor_action_type_2 is not '':
                action_data = [data_action_1, data_action_2]
            elif self.minor_action_type_1 is not '':
                action_data = [data_action_1]
            elif self.minor_action_type_2 is not '':
                action_data = [data_action_2]
        result = {
            'data_trigger': trigger_data,
            'trigger_detail_data': trigger_detail_data,
            'action_data': action_data,
        }
        return result

    def data_generate(self):
        """!@brief
        Generate all data, include of critical, major, minor
        @pre call when after generating critical data, major data and minor data
        @post return all data
        @return result: dictionary of all data
        """
        # 当A(column_a),B(column_b)在DB中查不到的时候， 说明数据不存在，不需要继续一下步骤，创建trigger失败。
        if self.expression_detail_result is False:
            return False
        result = {}
        insert_trigger = []
        insert_trigger_detail = []
        insert_action = []
        data_critical = self.data_generate_critical()
        data_major = self.data_generate_major()
        data_minor = self.data_generate_minor()
        if data_critical['data_trigger']:
            insert_trigger.append(data_critical['data_trigger'])
            insert_trigger_detail.append(data_critical['trigger_detail_data'])
            # insert_action.append(data_critical['action_data'])
            insert_action.append(data_critical['action_data'])
        if data_major['data_trigger']:
            insert_trigger.append(data_major['data_trigger'])
            insert_trigger_detail.append(data_major['trigger_detail_data'])
            # insert_action.append(data_major['action_data'])
            insert_action.append(data_major['action_data'])
        if data_minor['data_trigger']:
            insert_trigger.append(data_minor['data_trigger'])
            insert_trigger_detail.append(data_minor['trigger_detail_data'])
            # insert_action.append(data_minor['action_data'])
            insert_action.append(data_minor['action_data'])
        result['insert_trigger'] = insert_trigger
        result['insert_trigger_detail'] = insert_trigger_detail
        result['insert_action'] = insert_action
        return result

    def generate_trigger_detail_data(self, data, param):
        """!@brief
        Regenerate trigger detail data
        @param data: the data(type is list) of trigger detail
        @param param: the relationship of priority and trigger id, for getting corresponding relation
        of priority and trigger id
        @pre call when need to insert into trigger_detail table
        @post return trigger detail data(type is list)
        @return trigger_detail_data: list of trigger detail data
        """
        trigger_detail_data = []
        for per in data:
            priority_key = self.map_priority(per['priority'])
            per['trigger'] = param[priority_key]
            expression_in_trigger_detail = per['expression']
            for per_expression in expression_in_trigger_detail:
                per_trigger_detail_data = {
                    'expression': per_expression,
                    'status': per['status'],
                    'trigger': per['trigger'],
                    'expression_view': per['expression_view']
                }
                trigger_detail_data.append(per_trigger_detail_data)
        return trigger_detail_data

    def generate_action_data(self, data, param):
        """!@brief
        Regenerate action data
        @param data: the data of action
        @param param: the relationship of priority and trigger id, for getting corresponding relation
        of priority and trigger id
        @pre call when need to insert into actions table
        @post return action data(type is list)
        @return re_genreate_action_data: list of action data
        """
        re_genreate_action_data = []
        for per in data:
            for per_action in per:
                re_genreate_action_data.append(per_action)
        for per in re_genreate_action_data:
            priority_key = self.map_priority(per['priority'])
            per['trigger'] = param[priority_key]
        return re_genreate_action_data

    def get_search_sort_data(self, initial_data):
        """!@brief
        Generate sorted and searched data for summary page when need to sort or search
        @param initial_data: the initial data that no processing
        @pre call when the initial data is generated and need to sort and search
        @post return the data according the sort_by and search_by
        @return data: json of final view data
        """
        paginator = Paginator(initial_data, int(self.max_size_per_page))
        contacts = paginator.page(int(self.page_from))
        result = []
        search_data = {
            'name': self.action_policy_name_for_search,
            'trigger_type': self.trigger_type,
            'critical_priority': self.critical_priority,
            'column_a': self.column_a,
            'column_b': self.column_b,
            'device_group': self.device_group_name_for_search,
            'coll_policy_group': self.coll_policy_group_name_for_search,
            'major_priority': self.major_priority,
            'minor_priority': self.minor_priority,
            'desc': self.desc,
        }
        total_num = len(contacts.object_list)
        search_sort_data = {}
        for per in contacts.object_list:
            name = per['name']
            trigger_type = per['trigger_type']
            column = per['column']
            device_group = per['device_group']
            coll_policy_group = per['coll_policy_group']
            device_group_id = per['device_group_id']
            coll_policy_group_id = per['coll_policy_group_id']
            critical_priority = ''
            major_priority = ''
            minor_priority = ''
            if 'critical_priority' in per.keys():
                critical_priority = per['critical_priority']
            if 'major_priority' in per.keys():
                major_priority = per['major_priority']
            if 'minor_priority' in per.keys():
                minor_priority = per['minor_priority']
            desc = per['desc']
            if search_data['name'] and search_data['name'] not in name:
                continue
            if str(search_data['trigger_type']) and str(search_data['trigger_type']) != trigger_type:
                continue
            if search_data['critical_priority'] and search_data['critical_priority'] not in critical_priority:
                continue
            if search_data['major_priority'] and search_data['major_priority'] not in major_priority:
                continue
            if search_data['minor_priority'] and search_data['minor_priority'] not in minor_priority:
                continue
            if search_data['desc'] and search_data['desc'] not in desc:
                continue
            search_sort_data['name'] = name
            search_sort_data['trigger_type'] = trigger_type
            search_sort_data['column'] = column
            search_sort_data['device_group'] = device_group
            search_sort_data['device_group_id'] = device_group_id
            search_sort_data['coll_policy_group'] = coll_policy_group
            search_sort_data['coll_policy_group_id'] = coll_policy_group_id
            search_sort_data['critical_priority'] = critical_priority
            search_sort_data['major_priority'] = major_priority
            search_sort_data['minor_priority'] = minor_priority
            search_sort_data['desc'] = desc
            result.append(search_sort_data.copy())
        sort_by_list = ['name', 'trigger_type', 'critical_priority', 'major_priority', 'minor_priority', 'desc']
        if self.sort_by and self.sort_by in sort_by_list:
            if self.order:
                # True: asc, False: desc
                reverse = True
                if self.order.strip().lower() == 'asc'.strip().lower():
                    reverse = False
                result = sorted(result, key=lambda result: result[self.sort_by], reverse=reverse)
        data = {
            'data': {
                'data': result,
            },
            'new_token': self.new_token,
            'num_page': paginator.num_pages,
            # 'page_range': list(paginator.page_range),
            # 'page_has_next': contacts.has_next(),
            'total_num': total_num,
            'current_page_num': contacts.number,
            constants.STATUS: {
                constants.STATUS: constants.TRUE,
                constants.MESSAGE: constants.SUCCESS
            },
        }
        return data

    def generate_view_data(self):
        """!@brief
        Generate view data for summary page, then call get_search_sort_data to sort or search,
        and return the view data for display, if no need to sort or search, will display initial data
        @pre call from GET method
        @post return data for summary page
        @return result_data: json of view data
        """
        # queryset = Actions.objects.raw('select * from Actions group by action_name')
        # queryset = Actions.objects.values('action_name', 'trigger_id', 'trigger__priority', 'trigger__trigger_type',
        #                                   'trigger__descr').annotate(total_num=Count('action_name'))
        queryset = Actions.objects.values('action_name').annotate(total_num=Count('action_name'))
        # queryset_action_all = Actions.objects.filter(action_name__contains='SNMP')
        queryset_action_all = Actions.objects.filter()
        queryset_triggers = Triggers.objects.filter()
        # SELECT `actions`.`action_name`, COUNT(`actions`.`action_name`) AS `total_num` FROM `actions` GROUP BY `actions`.`action_name` ORDER BY NULL
        # print queryset.query
        view_list_data = []
        for per in queryset:
            action_name = per['action_name']
            result_in_trigger = queryset_triggers.filter(name=action_name)
            data_dic = {}
            priority_dic = {}
            column_a = ''
            column_b = ''
            device_group_a = ''
            device_group_b = ''
            device_group_a_id = ''
            device_group_b_id = ''
            coll_policy_group_a = ''
            coll_policy_group_b = ''
            coll_policy_group_a_id = ''
            coll_policy_group_b_id = ''
            for per_in_trigger in result_in_trigger:
                priority_dic[per_in_trigger.priority] = per_in_trigger.trigger_id
            data_dic['name'] = result_in_trigger[0].name
            data_dic['trigger_type'] = self.map_trigger_type(result_in_trigger[0].trigger_type)
            data_dic['desc'] = result_in_trigger[0].descr
            if result_in_trigger[0].columnA:
                column_a = DataTable.objects.get(table_id=int(result_in_trigger[0].columnA)).name
                device_group_a = DataTable.objects.get(table_id=int(result_in_trigger[0].columnA)).groups.name
                device_group_a_id = DataTable.objects.get(table_id=int(result_in_trigger[0].columnA)).groups.group_id
                coll_policy_group_a = \
                    DataTable.objects.filter(table_id=int(result_in_trigger[0].columnA)).values('policy_group__name')[
                        0]['policy_group__name']
                coll_policy_group_a_id = \
                    DataTable.objects.filter(table_id=int(result_in_trigger[0].columnA)).values('policy_group')[0][
                        'policy_group']
            if result_in_trigger[0].columnB:
                column_b = DataTable.objects.get(table_id=int(result_in_trigger[0].columnB)).name
                # device_group_b = DataTable.objects.get(table_id=int(result_in_trigger[0].columnB)).groups.name
                # device_group_b_id = DataTable.objects.get(table_id=int(result_in_trigger[0].columnB)).groups.group_id
                coll_policy_group_b = \
                    DataTable.objects.filter(table_id=int(result_in_trigger[0].columnB)).values('policy_group__name')[
                        0]['policy_group__name']
                coll_policy_group_b_id = \
                    DataTable.objects.filter(table_id=int(result_in_trigger[0].columnB)).values('policy_group')[0][
                        'policy_group']
            data_dic['column'] = str(column_a)
            if column_b:
                data_dic['column'] = str(column_a) + ',' + str(column_b)
            data_dic['device_group'] = str(device_group_a)
            data_dic['device_group_id'] = str(device_group_a_id)
            data_dic['coll_policy_group'] = str(coll_policy_group_a)
            if coll_policy_group_b:
                data_dic['coll_policy_group'] = str(coll_policy_group_a) + ',' + str(coll_policy_group_b)
            data_dic['coll_policy_group_id'] = str(coll_policy_group_a_id) + ',' + str(coll_policy_group_b_id)
            for per_priority in priority_dic:
                if per_priority == constants.NUMBER_ZERO:
                    data_dic['critical_priority'] = self.migrate(
                        queryset_action_all.filter(trigger_id=priority_dic[0]).values('action_type'))
                if per_priority == constants.NUMBER_ONE:
                    data_dic['major_priority'] = self.migrate(
                        queryset_action_all.filter(trigger_id=priority_dic[1]).values('action_type'))
                if per_priority == constants.NUMBER_TWO:
                    data_dic['minor_priority'] = self.migrate(
                        queryset_action_all.filter(trigger_id=priority_dic[2]).values('action_type'))
            view_list_data.append(data_dic)
        result_data = self.get_search_sort_data(view_list_data)
        return result_data

    def get_data_by_name(self):
        """!@brief
        When click [表示] button, generate data by action name
        @pre call from GET method when click [表示] button
        @post return the data according to the action name
        @return result: json of data
        """
        result_common = {}
        result_critical = {}
        result_major = {}
        result_minor = {}
        result_action_critical_list = []
        result_action_major_list = []
        result_action_minor_list = []
        # queryset_triggers = Triggers.objects.filter(name=self.action_policy_name)
        queryset_actions = Actions.objects.filter(action_name=self.action_policy_name_get_put_delete).values(
            'action_id',
            'action_type',
            'action_name',
            'snmp_version',
            'snmp_oid',
            'community',
            'ip_address',
            'username',
            'password',
            'command',
            'agent_address',
            'oid',
            'message',
            'param',
            'script_path',
            'status',
            'trigger_id',
            'trigger__descr',
            'trigger__trigger_type',
            'trigger__columnA',
            'trigger__columnB',
            'trigger__priority',
            'trigger__condition',
            'trigger__expression',
            'trigger__value',
            'trigger__trigger_limit_nums')
        # migrate_actions = queryset_actions.annotate(total_num=Count('action_name'))
        # print queryset_actions.query
        for per in queryset_actions:
            result_action_critical = {}
            result_action_major = {}
            result_action_minor = {}
            trigger_id = per['trigger_id']
            result_common['name'] = per['action_name']
            result_common['descr'] = per['trigger__descr']
            result_common['trigger_type'] = self.map_trigger_type(per['trigger__trigger_type'])
            result_common['columnA'] = DataTable.objects.get(table_id=int(per['trigger__columnA'])).name
            if per['trigger__columnB']:
                result_common['columnB'] = DataTable.objects.get(table_id=int(per['trigger__columnB'])).name
            priority = per['trigger__priority']
            if priority == constants.NUMBER_ZERO:
                result_critical['priority'] = self.map_priority(priority)
                result_critical['value'] = per['trigger__value']
                result_critical['condition'] = self.map_condition(per['trigger__condition'])
                result_critical['trigger_limit_nums'] = per['trigger__trigger_limit_nums']
                result_action_critical['action_type'] = per['action_type']
                result_action_critical['snmp_version'] = per['snmp_version']
                result_action_critical['snmp_oid'] = per['snmp_oid']
                result_action_critical['community'] = per['community']
                result_action_critical['ip_address'] = per['ip_address']
                result_action_critical['username'] = per['username']
                result_action_critical['password'] = per['password']
                result_action_critical['command'] = per['command']
                result_action_critical['agent_address'] = per['agent_address']
                result_action_critical['oid'] = per['oid']
                result_action_critical['message'] = per['message']
                result_action_critical['param'] = per['param']
                result_action_critical['script_path'] = per['script_path']
                result_action_critical['status'] = per['status']
                result_action_critical_list.append(result_action_critical)
            if priority == constants.NUMBER_ONE:
                result_major['priority'] = self.map_priority(priority)
                result_major['value'] = per['trigger__value']
                result_major['condition'] = self.map_condition(per['trigger__condition'])
                result_major['trigger_limit_nums'] = per['trigger__trigger_limit_nums']
                result_action_major['action_type'] = per['action_type']
                result_action_major['snmp_version'] = per['snmp_version']
                result_action_major['snmp_oid'] = per['snmp_oid']
                result_action_major['community'] = per['community']
                result_action_major['ip_address'] = per['ip_address']
                result_action_major['username'] = per['username']
                result_action_major['password'] = per['password']
                result_action_major['command'] = per['command']
                result_action_major['agent_address'] = per['agent_address']
                result_action_major['oid'] = per['oid']
                result_action_major['message'] = per['message']
                result_action_major['param'] = per['param']
                result_action_major['script_path'] = per['script_path']
                result_action_major['status'] = per['status']
                result_action_major_list.append(result_action_major)
            if priority == constants.NUMBER_TWO:
                result_minor['priority'] = self.map_priority(priority)
                result_minor['value'] = per['trigger__value']
                result_minor['condition'] = self.map_condition(per['trigger__condition'])
                result_minor['trigger_limit_nums'] = per['trigger__trigger_limit_nums']
                result_action_minor['action_type'] = per['action_type']
                result_action_minor['snmp_version'] = per['snmp_version']
                result_action_minor['snmp_oid'] = per['snmp_oid']
                result_action_minor['community'] = per['community']
                result_action_minor['ip_address'] = per['ip_address']
                result_action_minor['username'] = per['username']
                result_action_minor['password'] = per['password']
                result_action_minor['command'] = per['command']
                result_action_minor['agent_address'] = per['agent_address']
                result_action_minor['oid'] = per['oid']
                result_action_minor['message'] = per['message']
                result_action_minor['param'] = per['param']
                result_action_minor['script_path'] = per['script_path']
                result_action_minor['status'] = per['status']
                result_action_minor_list.append(result_action_minor)
        result = {
            'common_data': result_common,
            'critical': {
                'common_data': result_critical,
                'action_data': result_action_critical_list,
            },
            'major': {
                'common_data': result_major,
                'action_data': result_action_major_list,
            },
            'minor': {
                'common_data': result_minor,
                'action_data': result_action_minor_list,
            },
        }
        data = {
            'data': {
                'data': result
            },
            'new_token': self.new_token,
            constants.STATUS: {
                constants.STATUS: constants.TRUE,
                constants.MESSAGE: constants.SUCCESS
            },
        }
        return data

    def create_trigger_related(self, method='POST'):
        """!@brief
        Insert data into triggers table, actions table and trigger_detail table
        @pre call from POST or PUT method
        @post insert data into triggers table, actions table and trigger_detail table
        @return data: the status of whether insert successful, and inserted data for all tables
        """
        try:
            with transaction.atomic():
                data = self.data_generate()
                trigger_priority_dic = {}
                if data is False:
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLUMN_A_OR_COLUMN_B_NOT_EXIST
                        }
                    }
                    return api_return(data=data)
                # generate data for trigger table
                trigger = data['insert_trigger']
                # generate data for action table
                action = data['insert_action']
                # generate data for trigger detail table
                trigger_detail = data['insert_trigger_detail']
                if self.action_policy_name is not '':
                    get_name_from_cp = self.get_action_policy_in_trigger(**{'name': self.action_policy_name})
                    if len(get_name_from_cp) > constants.NUMBER_ZERO:
                        data = {
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.ACTION_POLICY_NAME_DUPLICATE
                            }
                        }
                        return api_return(data=data)
                serializer_trigger = TriggerSerializer(data=trigger, many=True)
                # save into triggers table
                if serializer_trigger.is_valid(Exception):
                    serializer_trigger.save()
                    for per in serializer_trigger.data:
                        trigger_id = per['trigger_id']
                        priority = self.map_priority(per['priority'])
                        trigger_priority_dic[priority] = trigger_id

                    # save into trigger_detail table
                    trigger_detail_data = self.generate_trigger_detail_data(trigger_detail, trigger_priority_dic)
                    serializer_trigger_detail = TriggerDetailSerializer(data=trigger_detail_data, many=True)
                    if serializer_trigger_detail.is_valid(Exception):
                        serializer_trigger_detail.save()

                    # save into action table
                    action_data = self.generate_action_data(action, trigger_priority_dic)
                    serializer_action = ActionsSerializer(data=action_data, many=True)
                    if serializer_action.is_valid(Exception):
                        serializer_action.save()
                    msg = constants.POST_SUCCESSFUL
                    if method == 'PUT':
                        msg = constants.PUT_SUCCESSFUL
                    data = {
                        'data': {
                            'trigger': serializer_trigger.data,
                            'trigger_detail': serializer_trigger_detail.data,
                            'action': serializer_action.data,
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: msg
                        }
                    }
                    return data
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def get(self):
        """!@brief
        Rest Api of GET, get all the data for summary page or get the data according to action name
        @return data: the data for summary page
        """
        try:
            if self.action_policy_name_get_put_delete is not '':
                result = self.get_data_by_name()
                return api_return(data=result)
            data = self.generate_view_data()
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        """!@brief
        Rest Api of POST, Insert data into triggers table, actions table and trigger_detail table
        @return data: the status of whether insert successful, and inserted data
        """
        try:
            with transaction.atomic():
                data = self.create_trigger_related(method='POST')
                if self.action_policy_name is not '':
                    pass
                    # mem cache
                    # data_for_mem_cache = MemCacheTriggerTriggerDetail().get(self.action_policy_name)
                    # with TriggerMemCache() as trigger:
                    #     trigger.multi_set(data_for_mem_cache)
                return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        """!@brief
        Rest Api of PUT, modify data according to action name
        @return data: the status of whether modify successful, and modified data
        """
        try:
            with transaction.atomic():
                print self.action_policy_name_get_put_delete, 222
                if self.action_policy_name_get_put_delete is not '':
                    # delete old trigger, trigger_detail, action data
                    self.delete_trigger_related(self.action_policy_name_get_put_delete)
                    # create new trigger, trigger_detail, action data
                    data = self.create_trigger_related(method='PUT')
                    # mem cache
                    # data_for_mem_cache = MemCacheTriggerTriggerDetail().get(self.action_policy_name)
                    # with TriggerMemCache() as trigger:
                    #     trigger.multi_set(data_for_mem_cache)
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        """!@brief
        Rest Api of DELETE, delete data according to action name
        @return data: the status of whether delete successful
        """
        try:
            with transaction.atomic():
                if self.action_policy_name_get_put_delete is not '':
                    self.delete_trigger_related(self.action_policy_name_get_put_delete)
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.DELETE_SUCCESSFUL
                        }
                    }
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
