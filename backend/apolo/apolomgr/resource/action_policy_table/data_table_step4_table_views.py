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
from backend.apolo.serializer.history_x_serializer import HistoryXSerializer
from backend.apolo.tools import constants


class DataTableTableViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableTableViewsSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        # coll_policy_rule_tree.treeid
        self.tree_id = views_helper.get_request_value(self.request, 'tree_id', 'GET')
        # collection policy id
        self.coll_policy_id = views_helper.get_request_value(self.request, 'coll_id', 'GET')
        # collection policy group id, schedule-->policy_group_id(coll_policy_groups)
        self.policy_group_id = views_helper.get_request_value(self.request, 'policy_group_id', 'GET')
        # device group id, from step2-->groups table(device_group_id)
        self.device_group_id = views_helper.get_request_value(self.request, 'device_group_id', 'GET')
        # schedule id
        self.schedule_id = views_helper.get_request_value(self.request, 'schedule_id', 'GET')
        # device ids
        self.devices = self.get_device_ids(**{'group': int(self.device_group_id)})
        # self.devices = views_helper.get_request_value(self.request, 'devices', 'GET')
        self.rule_name = views_helper.get_request_value(self.request, 'rule_name', 'GET')

    @staticmethod
    def get_history(item_id, value_type, policy_type):
        """!@brief
        Get history data from History%s%s table
        @param item_id: item id
        @param value_type: value type(str, int, float, text)
        @param policy_type: policy type(cli, snmp)
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
        history = table.objects.filter(**{"item_id": item_id}).order_by("-clock")
        if value_type not in trigger_numeric:
            for h in history:
                # h.value = "'" + h.value + "'"
                h.value = str(h.value)
        return history

    # @staticmethod
    # def get_mapping(code):
    #     """
    #     Search mapping relationship from Mapping table by given code
    #     :param code:
    #     :return: code meaning
    #     """
    #     value = Mapping.objects.filter(**{'code': code}).values('code_meaning')[0]
    #     return value['code_meaning']
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
        STRING = 3
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
            for device in self.devices:
                device_id = int(device['device'])
                result = {}
                # get policy type, 0:cli, 1:snmp
                policy_type = self.get_coll_policy(**{'coll_policy_id': self.coll_policy_id})
                kwargs = {
                    'coll_policy_rule_tree_treeid': self.tree_id,
                    'device': device_id,
                    'schedule': self.schedule_id,
                    'coll_policy': self.coll_policy_id,
                    'policys_groups': self.policy_group_id
                }
                if len(policy_type):
                    if int(policy_type[0]['policy_type']) == 1:
                        kwargs = {
                            'device': device_id,
                            'schedule': self.schedule_id,
                            'coll_policy': self.coll_policy_id,
                            'policys_groups': self.policy_group_id
                        }
                item_infos = Items.objects.filter(**kwargs).values('item_id', 'value_type', 'item_type',
                                                                   'device__hostname')
                if item_infos:
                    item_id = item_infos[0]['item_id']
                    value_type = self.get_mapping(item_infos[0]['value_type'])
                    item_type = self.get_mapping_cli_snmp(item_infos[0]['item_type'])
                    queryset = self.get_history(item_id, value_type, item_type)
                    serializer = HistoryXSerializer(queryset, many=True)
                    if serializer.data:
                        result['device_name'] = item_infos[0]['device__hostname']
                        result['time_stamp'] = serializer.data[0]['clock']
                        result['path'] = serializer.data[0]['block_path']
                        result['value'] = serializer.data[0]['value']
                        result['item_id'] = serializer.data[0]['item']
                        result['rule_name'] = self.rule_name
                        data.append(result)
            data = {
                'data': {
                    'data': data,
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
