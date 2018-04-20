#!/usr/bin/env python
# coding=utf-8
"""

@author: necwang
@contact: necwang@cisco.com
@file: data_table_step4_table_views.py
@time: 2018/1/15 16:34
@desc:

"""

import traceback
import importlib
from rest_framework import viewsets

from backend.apolo.models import Items, DevicesGroups, CollPolicy
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import views_helper
from backend.apolo.tools import constants
import time
from django.db import connection


class DataTableTableViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableTableViewsSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        # coll_policy_rule_tree.treeid
        self.tree_id = views_helper.get_request_value(self.request, 'tree_id', 'GET')
        # collection policy id
        self.coll_policy_id = views_helper.get_request_value(self.request, 'coll_id', 'GET')
        # collection policy group id, schedule-->policy_group_id(coll_policy_groups), not use anymore
        # self.policy_group_id = views_helper.get_request_value(self.request, 'policy_group_id', 'GET')
        # device group id, from step2-->groups table(device_group_id)
        self.device_group_id = views_helper.get_request_value(self.request, 'device_group_id', 'GET')
        # schedule id
        self.schedule_id = views_helper.get_request_value(self.request, 'schedule_id', 'GET')
        # device ids
        self.devices = self.get_device_ids(**{'group': int(self.device_group_id)})
        # self.devices = views_helper.get_request_value(self.request, 'devices', 'GET')
        # self.rule_name = views_helper.get_request_value(self.request, 'rule_name', 'GET')
        self.oid = views_helper.get_request_value(self.request, 'oid', 'GET')

    def get_history(self, item_id, value_type, policy_type):
        """!@brief
        Get history data from history_%s_%s table
        @param item_id: item id
        @param value_type: value type(str, int, float, text)
        @param policy_type: policy type(cli, snmp)
        @note
        @return history: history data(type is dic)
        """
        try:
            base_db_format = "history_%s_%s"
            table_name = base_db_format % (policy_type.lower(), value_type.lower())
            where_condition = 'item_id = ' + str(item_id)
            with connection.cursor() as cursor:
                sql = "select * from %s where %s order by %s" % (table_name, where_condition, '-clock')
                cursor.execute(sql)
                # cursor.execute("SELECT * FROM history_cli_str LIMIT 2")
                return self.dict_fetchall(cursor)
                # history = table.objects.filter(**kwargs).order_by("-clock")
                # if value_type not in trigger_numeric:
                #     for h in history:
                #         # h.value = "'" + h.value + "'"
                #         h.value = str(h.value)
                # return history
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def dict_fetchall(_cursor):
        columns = [col[0] for col in _cursor.description]
        return [
            dict(zip(columns, row))
            for row in _cursor.fetchall()
            ]

    @staticmethod
    def get_device_ids(**kwargs):
        """!@brief
        Get the device ids as group_id of the DevicesGroups table
        @param kwargs: dictionary type of the query condition
        @pre call when need to select DevicesGroups table
        @post according to the need to deal with the DevicesGroups table
        @note
        @return result: queryset of DevicesGroups table
        """
        try:
            result = DevicesGroups.objects.filter(**kwargs).values('device')
            return result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_coll_policy(**kwargs):
        """!@brief
        Get the device ids as group_id of the CollPolicy table
        @param kwargs: dictionary type of the query condition
        @pre call when need to select CollPolicy table
        @post according to the need to deal with the CollPolicy table
        @note
        @return result: queryset of CollPolicy table
        """
        try:
            result = CollPolicy.objects.filter(**kwargs).values('policy_type')
            return result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_mapping(code):
        """!@brief
        Match the value type， change the integer value into string value,
        INT = 0
        TEXT = 1
        FLOAT = 2
        STR = 3
        @param code: the integer value of value type
        @pre call when need to change value type
        @post return the value type
        @return code_meaning: string value type

        """
        # value = Mapping.objects.filter(**{'code': code}).values('code_meaning')[0]
        code_meaning = ''
        if code == constants.NUMBER_ZERO:
            code_meaning = constants.INTEGER
        if code == constants.NUMBER_ONE:
            code_meaning = constants.TEXT
        if code == constants.NUMBER_TWO:
            code_meaning = constants.FLOAT
        if code == constants.NUMBER_THREE:
            code_meaning = constants.STRING
        return code_meaning

    @staticmethod
    def get_mapping_cli_snmp(code):
        """!@brief
        Match the value type， change the integer value into string value,
        0: cli, 1: snmp
        @param code: the integer value of value type
        @pre call when need to change value type
        @post return the value type
        @return code_meaning: string value type
        """
        # value = Mapping.objects.filter(**{'code': code}).values('code_meaning')[0]
        code_meaning = ''
        if code == constants.NUMBER_ZERO:
            code_meaning = constants.CLI
        if code == constants.NUMBER_ONE:
            code_meaning = constants.SNMP
        return code_meaning

    def get(self):
        """!@brief
        Get data in right for Step 4 when click [新规登陆]
        Get the latest history data of each device for right table in step 4
        @return data: data for right table in step 4
        """
        try:
            data = []
            items_rule_name_list = []
            for device in self.devices:
                device_id = int(device['device'])
                result = {}
                item_rule_name_dic = {}
                # get policy type, 0:cli, 1:snmp
                policy_type = self.get_coll_policy(**{'coll_policy_id': self.coll_policy_id})
                kwargs = {
                    'coll_policy_rule_tree_treeid': self.tree_id,
                    'device': device_id,
                    'schedule': self.schedule_id,
                    'coll_policy': self.coll_policy_id,
                    # 'policys_groups__policy_group': self.policy_group_id
                }
                if len(policy_type):
                    # snmp
                    if int(policy_type[0]['policy_type']) == 1:
                        kwargs = {
                            'device': device_id,
                            'schedule': self.schedule_id,
                            'coll_policy': self.coll_policy_id,
                            # 'policys_groups__policy_group': self.policy_group_id
                        }
                item_infos = Items.objects.filter(**kwargs).values('item_id',
                                                                   'value_type',
                                                                   'item_type',
                                                                   'device__hostname',
                                                                   'coll_policy_rule_tree_treeid__rule__key_str')
                if item_infos:
                    rule_name = item_infos[0]['coll_policy_rule_tree_treeid__rule__key_str']
                    item_id = item_infos[0]['item_id']
                    value_type = self.get_mapping(item_infos[0]['value_type'])
                    item_type = self.get_mapping_cli_snmp(item_infos[0]['item_type'])
                    history_data = self.get_history(item_id, value_type, item_type)
                    item_rule_name_dic['item_id'] = item_id
                    item_rule_name_dic['rule_name'] = rule_name
                    items_rule_name_list.append(item_rule_name_dic)
                    if history_data:
                        result['device_name'] = item_infos[0]['device__hostname']
                        # result['time_stamp'] = serializer.data[0]['clock']
                        result['time_stamp'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                             time.localtime(int(history_data[0]['clock'])))
                        if item_type.upper() == 'CLI':
                            result['path'] = history_data[0]['block_path']
                        result['value'] = history_data[0]['value']
                        # result['item_id'] = serializer.data[0]['item']
                        # result['rule_name'] = rule_name
                        if len(policy_type):
                            if int(policy_type[0]['policy_type']) == 1:
                                result['oid'] = self.oid
                        data.append(result)
            data = {
                'data': {
                    'data': data,
                    'items_rule_name': items_rule_name_list
                },
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS,
                },
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
