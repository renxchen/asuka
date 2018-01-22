#!/usr/bin/env python
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
        history = table.objects.filter(**{"item_id": item_id}).order_by("-clock")
        if value_type not in trigger_numeric:
            for h in history:
                # h.value = "'" + h.value + "'"
                h.value = str(h.value)
        return history

    @staticmethod
    def get_mapping(code):
        """
        Search mapping relationship from Mapping table by given code
        :param code:
        :return: code meaning
        """
        value = Mapping.objects.filter(**{'code': code}).values('code_meaning')[0]
        return value['code_meaning']

    def get(self):
        """
        Get the latest history data of each device in right table of action policy step 4
        API: http://127.0.0.1:1111/v1/api_data_table_table/?id=17&devices=1,2&coll_id=2&rule_name=RP0
        :return: latest history data of each device
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
            print traceback.format_exc(e)
            return exception_handler(e)
