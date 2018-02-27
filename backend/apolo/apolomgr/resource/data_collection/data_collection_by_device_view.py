#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_by_device_view.py
@time: 2018/1/16 11:13
@desc:

'''
from django.db import transaction
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.tool import Tool
from backend.apolo.models import Devices, Items
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class DataCollectionByDeviceViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataCollectionByDeviceViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    def get(self):
        # http://127.0.0.1:8000/v1/api_data_collection_devices/?device_id=3
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
            # response_json_data = Tool.get_data_from_collection_server()
            # arry = []
            # cp_group_line_rowspan_dict = dict()
            # device_line_rowspan = 0
            # # device_id = 1
            # table_dict = dict()
            # for one_recoder in response_json_data['items']:
            #     if one_recoder['device_id'] == device_id:
            #         device_line_rowspan += 1
            #         cp_group_name = one_recoder['policy_group_name']
            #         if cp_group_line_rowspan_dict.has_key(cp_group_name):
            #             cp_group_line_rowspan_dict[cp_group_name] += 1
            #         else:
            #             cp_group_line_rowspan_dict.update({cp_group_name: 1})
            #
            #         if table_dict.has_key(cp_group_name):
            #             table_dict[cp_group_name].append(
            #                 {
            #                     "item_id": one_recoder['item_id'],
            #                     "valid_status": one_recoder['valid_status'],
            #                     'policyNo': one_recoder['coll_policy_id'],
            #                     'cpGroup': cp_group_name,
            #                     'device': one_recoder['device_name'],
            #                     'priority': Tool.set_priority_mapping(one_recoder['priority']),
            #                     'policy': '{} {}'.format(one_recoder['policy_name'], one_recoder['exec_interval']),
            #                     'attr': {
            #                         'device': {
            #                             'rowspan': None
            #                         },
            #                         'cpGroup': {
            #                             'rowspan': None
            #                         },
            #                         'priority': {
            #                             'rowspan': None
            #                         }
            #                     }
            #                 })
            #         else:
            #             table_dict[cp_group_name] = [{
            #                     "item_id": one_recoder['item_id'],
            #                     "valid_status": one_recoder['valid_status'],
            #                     'policyNo': one_recoder['coll_policy_id'],
            #                     'cpGroup': cp_group_name,
            #                     'device': one_recoder['device_name'],
            #                     'priority': Tool.set_priority_mapping(one_recoder['priority']),
            #                     'policy': '{} {}'.format(one_recoder['policy_name'], one_recoder['exec_interval']),
            #                     'attr': {
            #                         'device': {
            #                             'rowspan': None
            #                         },
            #                         'cpGroup': {
            #                             'rowspan': None
            #                         },
            #                         'priority': {
            #                             'rowspan': None
            #                         }
            #                     }
            #                 }]
            # is_the_first_device = True
            # for k, v in table_dict.items():
            #     for recoder in v:
            #         if is_the_first_device:
            #             is_the_first_device = False
            #             recoder['attr']['device']['rowspan'] = device_line_rowspan
            #         if cp_group_line_rowspan_dict.has_key(k):
            #             recoder['attr']['cpGroup']['rowspan'] = cp_group_line_rowspan_dict[k]
            #             recoder['attr']['priority']['rowspan'] = cp_group_line_rowspan_dict[k]
            #             del cp_group_line_rowspan_dict[k]
            #         arry.append(recoder)
            arry =self.__set_items_info_by_device(device_id)
            data = {
                'data': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)


    def put(self):
        # http://127.0.0.1:8000/v1/api_data_collection_devices/
        # http://127.0.0.1:8000/v1/api_data_collection_devices/
        # {"item_list":[1,2,3,],"status":0,"device_id":1}
        item_list = views_helper.get_request_value(self.request, 'item_list', 'BODY')
        item_status = int(views_helper.get_request_value(self.request, 'status', 'BODY'))
        device_id = int(views_helper.get_request_value(self.request, 'device_id', 'BODY'))
        try:
            Items.objects.filter(item_id__in=item_list).update(status=item_status)
            arry = self.__set_items_info_by_device(device_id)
            data = {
                'data': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        except Exception as e:
            print e
            return exception_handler(e)


    @staticmethod
    def __set_items_info_by_device(device_id):
        response_json_data = Tool.get_data_from_collection_server()
        arry = []
        cp_group_line_rowspan_dict = dict()
        device_line_rowspan = 0
        # device_id = 1
        table_dict = dict()
        for one_recoder in response_json_data['items']:
            if one_recoder['device_id'] == device_id:
                device_line_rowspan += 1
                cp_group_name = one_recoder['policy_group_name']
                if cp_group_line_rowspan_dict.has_key(cp_group_name):
                    cp_group_line_rowspan_dict[cp_group_name] += 1
                else:
                    cp_group_line_rowspan_dict.update({cp_group_name: 1})

                if table_dict.has_key(cp_group_name):
                    table_dict[cp_group_name].append(
                        {
                            "item_id": one_recoder['item_id'],
                            "valid_status": one_recoder['valid_status'],
                            'policyNo': one_recoder['coll_policy_id'],
                            'cpGroup': cp_group_name,
                            'device': one_recoder['device_name'],
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
                else:
                    table_dict[cp_group_name] = [{
                        "item_id": one_recoder['item_id'],
                        "valid_status": one_recoder['valid_status'],
                        'policyNo': one_recoder['coll_policy_id'],
                        'cpGroup': cp_group_name,
                        'device': one_recoder['device_name'],
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
                    }]
        is_the_first_device = True
        for k, v in table_dict.items():
            for recoder in v:
                if is_the_first_device:
                    is_the_first_device = False
                    recoder['attr']['device']['rowspan'] = device_line_rowspan
                if cp_group_line_rowspan_dict.has_key(k):
                    recoder['attr']['cpGroup']['rowspan'] = cp_group_line_rowspan_dict[k]
                    recoder['attr']['priority']['rowspan'] = cp_group_line_rowspan_dict[k]
                    del cp_group_line_rowspan_dict[k]
                arry.append(recoder)
        return arry

