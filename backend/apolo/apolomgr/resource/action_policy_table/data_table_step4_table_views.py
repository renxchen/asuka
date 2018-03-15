#!/usr/bin/env python
# coding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: data_table_step4_table_views.py
@time: 2018/1/15 16:34
@desc:

"""

import traceback
import importlib
from rest_framework import viewsets
from django.utils.translation import gettext

from backend.apolo.models import Items, Mapping
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import views_helper
from backend.apolo.serializer.history_x_serializer import HistoryXSerializer
from backend.apolo.tools import constants


class DataTableTableViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableTableViewsSet, self).__init__(**kwargs)
        self.request = request
        # coll_policy_rule_tree.treeid
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        # collection policy id
        self.coll_policy_id = views_helper.get_request_value(self.request, 'coll_id', 'GET')
        # device ids
        self.devices = views_helper.get_request_value(self.request, 'devices', 'GET')
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

    def get(self):
        """!@brief
        Get data in right for Step 4 when click [新规登陆]
        Get the latest history data of each device for right table in step 4
        @return data: data for right table in step 4
        """
        try:
            data = []
            if self.id is not '':
                for device_id in self.devices.split(','):
                    result = {
                        'device_name': '',
                        'time_stamp': '',
                        'path': '',
                        'value': '',
                        'item_id': '',
                        'rule_name': ''
                    }
                    item_infos = Items.objects.filter(
                        **{'coll_policy_rule_tree_treeid': self.id, 'device': device_id,
                           'coll_policy': self.coll_policy_id}).values('item_id', 'value_type', 'item_type',
                                                                       'device__hostname')
                    item_id = item_infos[0]['item_id']
                    value_type = self.get_mapping(item_infos[0]['value_type'])
                    item_type = self.get_mapping(item_infos[0]['item_type'])
                    queryset = self.get_history(item_id, value_type, item_type)
                    serializer = HistoryXSerializer(queryset, many=True)
                    result['device_name'] = item_infos[0]['device__hostname']
                    result['time_stamp'] = serializer.data[0]['clock']
                    result['path'] = serializer.data[0]['block_path']
                    result['value'] = serializer.data[0]['value']
                    result['item_id'] = serializer.data[0]['item']
                    result['rule_name'] = self.rule_name
                    data.append(result)
                return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
