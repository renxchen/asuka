#!/usr/bin/env python

'''

@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: data_collection_by_device_view.py
@time: 2018/1/16 11:13
@desc:

'''
from django.db import transaction
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.models import Devices, Items, PolicysGroups, DevicesGroups, Schedules
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
        device_id = views_helper.get_request_value(self.request, 'device_id', 'GET')
        # load devices list,init action
        if not device_id:
            devices_list = Devices.objects.filter(status=1).values('device_id', 'hostname')
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

    def put(self):
        # http://127.0.0.1:8000/v1/api_data_collection_devices/
        # request param: is_all,coll_policy_id,device_id,policy_group_id,status
        # is_all =1: all stop,is_all = 0:stop some item
        is_all = int(views_helper.get_request_value(self.request, 'is_all', 'BODY'))
        coll_policy_id = views_helper.get_request_value(self.request, 'coll_policy_id', 'BODY')
        device_id = views_helper.get_request_value(self.request, 'device_id', 'BODY')
        status = int(views_helper.get_request_value(self.request, 'status', 'BODY'))
        policy_group_id = int(views_helper.get_request_value(self.request, 'policy_group_id', 'BODY'))

        try:
            if is_all == 1:
                # stop all items of the device
                Items.objects.filter(device=device_id).update(status=status)
            else:
                policys_groups_id_queryset = PolicysGroups.objects.filter(policy=coll_policy_id,
                                                                          policy_group=policy_group_id)

                with transaction.atomic():
                    for obj in policys_groups_id_queryset:
                        Items.objects.filter(device=device_id,
                                             coll_policy=obj.policy,
                                             policys_groups=obj.policys_groups_id).update(status=status)

            data = {
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
        valid_items_dict = Tool.get_valid_item({"policys_groups__status": 1, "device__device_id": device_id})
        # get all function off schedule by device_id
        device_group_id_arry = DevicesGroups.objects.filter(device=device_id).values("group_id")
        function_off_schedules = Schedules.objects.filter(device_group__in=device_group_id_arry, status=0,
                                                          policy_group=None).values()

        function_off_device_group_dict = dict()
        for schedule in function_off_schedules:
            if not function_off_device_group_dict.has_key(schedule['device_group_id']):
                function_off_device_group_dict.update({schedule['device_group_id']: schedule})

        arry = []
        item_stop_dict = dict()
        table_dict = dict()
        for one_recoder in valid_items_dict:

            device_group_name = one_recoder['device_group_name']
            device_group_id = one_recoder['device_group_id']
            cp_group_name = one_recoder['policy_group_name']
            cp_priority = Tool.set_priority_mapping(one_recoder['priority'])
            if table_dict.has_key(device_group_name):
                if table_dict[device_group_name].has_key(cp_group_name):
                    if table_dict[device_group_name][cp_group_name].has_key(cp_priority):
                        table_dict[device_group_name][cp_group_name][cp_priority].append(one_recoder)
                    else:
                        table_dict[device_group_name][cp_group_name].update({cp_priority: [one_recoder]})
                else:
                    table_dict[device_group_name].update({cp_group_name: {cp_priority: [one_recoder]}})
            else:
                table_dict.update({device_group_name: {cp_group_name: {cp_priority: [one_recoder]}}})


            # add all function off
            if function_off_device_group_dict.has_key(device_group_id):
                table_dict[device_group_name].update({-1: {-1: [function_off_device_group_dict[device_group_id]]}})

        start_index = 0
        for dgp_name, dgp_obj in table_dict.items():
            dpg_rowspan = 0
            dpg_rowspan_flag = True
            dpg_start_index = 0
            for cpg_name, cpg_obj in dgp_obj.items():
                cpg_rowspan = 0
                cpg_rowspan_flag = True
                cpg_start_index = 0
                for priority_name, priority_obj in cpg_obj.items():
                    priority_rowspan = 0
                    priority_rowspan_flag = True
                    priority_start_index = 0
                    for entry in priority_obj:
                        dpg_rowspan +=1
                        cpg_rowspan +=1
                        priority_rowspan +=1

                        if cpg_name !=-1:
                            data = {
                                "item_id": entry['item_id'],
                                "valid_status": entry['valid_status'],
                                "btn_status": entry['btn_status'],
                                'policyNo': entry['coll_policy_id'],
                                'cpGroup': entry['policy_group_name'],
                                'cpGroupNo': entry['policy_group_id'],
                                'device': entry['device_name'],
                                'deviceGroupNo': entry['device_group_id'],
                                'deviceGroup': entry['device_group_name'],
                                'priority': Tool.set_priority_mapping(entry['priority']),
                                'policy': '{}  {}'.format(entry['policy_name'], entry['exec_interval']),
                                'attr': {
                                    'deviceGroup': {
                                        'rowspan': None
                                    },
                                    'cpGroup': {
                                        'rowspan': None
                                    },
                                    'priority': {
                                        'rowspan': None
                                    }
                                }
                            }
                            if entry['item_status'] == 0:
                                data1 = {
                                    "item_id": entry['item_id'],
                                    "valid_status": True,
                                    "btn_status": -1,
                                    'policyNo': -1,
                                    'cpGroup': '{}_{}'.format(dgp_name, constants.EMERGENCY_STOP),
                                    'cpGroupNo': -1,
                                    'device': entry['device_name'],
                                    'deviceGroupNo': -1,
                                    'deviceGroup': constants.EMERGENCY_STOP,
                                    'priority': constants.PRIORITY_URGENT_LEVEL_KEY,
                                    'policy': '{}  {}'.format(entry['policy_name'], constants.EMERGENCY_STOP),
                                    'attr': {
                                        'deviceGroup': {
                                            'rowspan': None
                                        },
                                        'cpGroup': {
                                            'rowspan': None
                                        },
                                        'priority': {
                                            'rowspan': None
                                        }
                                    }
                                }
                                stop_key = '{}_{}'.format(dgp_name, entry['policy_name'])
                                if item_stop_dict.has_key(stop_key):
                                    pass
                                else:
                                    item_stop_dict.update({stop_key: data1})
                        else:
                            data = {
                                "item_id": None,
                                "valid_status": 1,
                                "btn_status": -1,
                                'policyNo': None,
                                'cpGroup': '{}_{}'.format(dgp_name, constants.ALL_FUNCTION_OFF),
                                'cpGroupNo': None,
                                'device': None,
                                'deviceGroupNo': entry['device_group_id'],
                                'deviceGroup': dgp_name,
                                'priority': Tool.set_priority_mapping(entry['priority']),
                                'policy': constants.ALL_FUNCTION_OFF,
                                'attr': {
                                    'deviceGroup': {
                                        'rowspan': None
                                    },
                                    'cpGroup': {
                                        'rowspan': None
                                    },
                                    'priority': {
                                        'rowspan': None
                                    }
                                }
                            }
                        if dpg_rowspan_flag:
                            dpg_start_index = start_index
                            dpg_rowspan_flag = False
                        if cpg_rowspan_flag:
                            cpg_start_index = start_index
                            cpg_rowspan_flag = False
                        if priority_rowspan_flag:
                            priority_start_index = start_index
                            priority_rowspan_flag = False

                        arry.append(data)
                        start_index += 1

                    arry[priority_start_index]['attr']['priority']['rowspan'] = priority_rowspan

                arry[cpg_start_index]['attr']['cpGroup']['rowspan'] = cpg_rowspan

            arry[dpg_start_index]['attr']['deviceGroup']['rowspan'] = dpg_rowspan
        if len(item_stop_dict) > 0:
            item_stop_list = item_stop_dict.values()
            item_stop_list[0]['attr']['deviceGroup']['rowspan']=len(item_stop_list)
            item_stop_list[0]['attr']['cpGroup']['rowspan'] = len(item_stop_list)
            item_stop_list[0]['attr']['priority']['rowspan'] = len(item_stop_list)
            arry.extend(item_stop_list)
        return arry
