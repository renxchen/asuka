#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: necwang
@contact: necwang@cisco.com
@file: mem_cache_trigger_and_trigger_detial.py
@time: 2018/3/27 17:34
@desc:

"""
import traceback
from rest_framework import viewsets
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.models import Triggers, TriggerDetail, DataTableItems
import logging
from django.db.models import *


class MemCacheTriggerTriggerDetail(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super(MemCacheTriggerTriggerDetail, self).__init__(**kwargs)
        self.logger = logging.getLogger("apolo.log")

    @staticmethod
    def get_trigger(action_name=None):
        """!@brief
        Get the queryset of the Trigger table
        @pre call when need to select Trigger table
        @post according to the need to deal with the Trigger table
        @note
        @return result: queryset of Trigger table
        """
        try:
            kwarg = {}
            if action_name is not None:
                kwarg = {'name': action_name}
            result = Triggers.objects.filter(**kwarg).values('name', 'trigger_id', 'columnA')
            return result
        except Exception as e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_data_table_item(**kwargs):
        """!@brief
        Get the queryset of the DataTableItems table
        @pre call when need to select DataTableItems table
        @post according to the need to deal with the DataTableItems table
        @note
        @return result: queryset of DataTableItems table
        """
        try:
            result = DataTableItems.objects.filter(**kwargs).values('item__device__device_id').annotate(
                total_num=Count('item__device__device_id'))
            return result
        except Exception as e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_trigger_detail(trigger_id=None):
        """!@brief
        Get the queryset of the TriggerDetail table
        @pre call when need to select TriggerDetail table
        @post according to the need to deal with the TriggerDetail table
        @note
        @return result: queryset of TriggerDetail table
        """
        try:
            kwargs = {}
            if trigger_id is not None:
                kwargs = {'trigger_id': trigger_id}
            result = TriggerDetail.objects.filter(**kwargs).values('expression', 'itemA', 'itemB')
            return result
        except Exception as e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def prepare_data_for_memory_cache(self, action_name=None):
        initial_data = []
        trigger_dic = {}
        trigger_column_expression_dic = {}
        try:
            '''
            step 1：
            # 根据action_name查询triggers表， 默认action_name为None，即查所有.
            # 返回字典{triggerid:columnA}.
            1. select triggers according the action_name, action_name is None by default(if action_name is None,
               will return all triggers).
            2. return dic {triggerid: columnA}.
            '''
            trigger_data = self.get_trigger(action_name)
            for per_trigger in trigger_data:
                key = str(per_trigger['trigger_id'])
                trigger_dic[key] = str(per_trigger['columnA'])

            '''
            step 2：
            # 根据step 1返回的trigger_dic中的trigger_id， 查询trigger_detail表中对应的expression.
            # 返回字典{triggerid_columnA: [{'trigger_id':triggerid, 'exception':expression, 'itemA':itemA, 'itemB':itemB}]}
            1. select trigger_detail according the trigger_id from the return value trigger_dic of step 1,
               get the corresponding expression.
            2. return dic {triggerid_columnA: [{'trigger_id':triggerid, 'exception':expression, 'itemA':itemA, 'itemB':itemB}]}
            '''
            for key, value in trigger_dic.items():
                temp_trigger_exp_lst = []
                trigger_id = key
                trigger_column_key = str(trigger_id) + '_' + str(value)
                trigger_detail = self.get_trigger_detail(trigger_id)
                for per_trigger_detail in trigger_detail:
                    temp_trigger_exp_lst.append(
                        [{
                            'trigger_id': trigger_id,
                            'exception': per_trigger_detail['expression'],
                            'itemA': per_trigger_detail['itemA'],
                            'itemB': per_trigger_detail['itemB']}
                        ])
                trigger_column_expression_dic[trigger_column_key] = temp_trigger_exp_lst

            '''
            step 3：
            # 根据step 2返回的trigger_column_expression_dic中的columnA， 查询data_table_item表中对应的device.
            # 返回所有columnA对应的device，
            # 格式{deviceid: [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}]}.
            1. select data_table_item according the columnA from the return value rigger_column_expression_dic of step 2,
               get the corresponding device.
            2. return dic {deviceid: [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}]}.
            '''
            for key, value in trigger_column_expression_dic.items():
                device_trigger_exp_dic = {}
                columnA = key.split('_')[1]
                trigger_expression_list = value
                devices = self.get_data_table_item(**{'table_id': int(columnA)})
                for per_device in devices:
                    device_id = per_device['item__device__device_id']
                    device_trigger_exp_dic[str(device_id)] = str(trigger_expression_list)
                initial_data.append(device_trigger_exp_dic)
            '''
            step 4：
            # 根据step 3返回的initial_data, 生成所有device与expression的对应关系.
            # 返回结果
            {
                deviceid1: [
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}],
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}]
                           ]
                deviceid2: [
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}],
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}]
                           ]
            }
            1. integrate the relationship of every device and [trigger,expression].
            2. return dic
            {
                deviceid1: [
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}],
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}]
                           ]
                deviceid2: [
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}],
                            [{trigger_id: triggerid, expression:expression, itemA:itemA, itemB:itemB}]
                           ]
            }
            '''
            integrated_device_trigger_exp_dic = {}
            for per in initial_data:
                for key, value in per.items():
                    if key in integrated_device_trigger_exp_dic.keys():
                        tmp = integrated_device_trigger_exp_dic[key] + eval(value)
                        integrated_device_trigger_exp_dic[key] = tmp
                    else:
                        integrated_device_trigger_exp_dic[key] = eval(value)
            return integrated_device_trigger_exp_dic
        except Exception as e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def get(self, action_name=None):
        """!@brief
        Rest Api of GET, get all the data for summary page or get the data according to action name
        @return data: the data for summary page
        """
        try:
            data = self.prepare_data_for_memory_cache(action_name)
            return api_return(data=data)
        except Exception as e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
