#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_by_device_view.py
@time: 2018/1/16 11:13
@desc:

'''
import json

import time
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.tool import Tool
from backend.apolo.models import Devices
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.views_helper import api_return
import requests


class DataCollectionByDeviceViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataCollectionByDeviceViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    def get(self):
        # http: // 127.0.0.1:8000/v1/api_data_collection_devices/?device_id = 1
        device_id = int(views_helper.get_request_value(self.request, 'device_id', 'GET'))
        # load devices list,init action
        if not device_id:
            devices_list = Devices.objects.values('device_id', 'hostname')
            arry = []
            for item in devices_list:
                arry.append(item)
            data = {
                'devices': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        else:
            response_json_data = self.__get_data_from_collection_server__()
            arry = []
            cp_group_line_rowspan_dict = dict()
            device_line_rowspan = 0
            for one_recoder in response_json_data['items']:
                if one_recoder['device_id'] == device_id:
                    device_line_rowspan +=1
                    cp_group_name = one_recoder['policy_group_name']
                    if cp_group_line_rowspan_dict.has_key(cp_group_name):
                        cp_group_line_rowspan_dict = {cp_group_name: 1}
                    else:
                        cp_group_line_rowspan_dict[cp_group_name] = 1
                    arry.append({
                        "valid_status": one_recoder['valid_status'],
                        'policyNo': one_recoder['coll_policy_id'],
                        'device': one_recoder['device_name'],
                        'cpGroup': cp_group_name,
                        'priority': Tool.set_priority_mapping(one_recoder['priority']),
                        'policy': '{} {}'.format(one_recoder['policy_name'], one_recoder['exec_interval']),
                        'attr': {
                            'device': {
                                'rowspan': None
                            },
                            'cpGroup': {
                                'rowspan': None
                            },
                            'priority': {
                                'rowspan': None
                            }
                        }
                    })
            if len(arry) >0:
                arry[0]['attr']['device']['rowspan'] = device_line_rowspan
                for item in arry:
                    cp_group_name = item['cpGroup']
                    if cp_group_line_rowspan_dict.has_key(cp_group_name):
                        item['attr']['cpGroup']['rowspan'] = cp_group_line_rowspan_dict[cp_group_name]
                        item['attr']['priority']['rowspan'] = cp_group_line_rowspan_dict[cp_group_name]
                        del cp_group_line_rowspan_dict[cp_group_name]

            data = {
                'data': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)

    @staticmethod
    def __get_data_from_collection_server__():
        now_time = int(time.time())
        json_data = json.dumps({"now_time": now_time, "item_type": -1})
        response = requests.post(constants.DATA_COLLECTION_POST_URL, data=json_data)
        return response.json()

    def put(self):
        pass
