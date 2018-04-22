#!/usr/bin/env python

"""
@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: emergency_stop_list_view.py
@time: 2018/4/13 14:53
@desc:

"""
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class EmergencyStopListViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(EmergencyStopListViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')


    def get(self):

        device_name = views_helper.get_request_value(self.request, 'device', 'GET')
        try:

            emergency_stop_list = Tool.get_emergency_stop_list(device_name)
            arry = self.__set_emergency_stop_list_table_view(emergency_stop_list)
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
    def __set_emergency_stop_list_table_view(emergency_stop_list):
        # set data
        table_dict = dict()
        for item in emergency_stop_list:
            device_name = item['device_name']
            cpg_name = item['policy_group_name']
            dgp_name = item['device_group_name']
            priority = item['priority']

            if table_dict.has_key(device_name):
                if table_dict[device_name].has_key(dgp_name):
                    if table_dict[device_name][dgp_name].has_key(cpg_name):
                        if table_dict[device_name][dgp_name][cpg_name].has_key(priority):
                            table_dict[device_name][dgp_name][cpg_name][priority].append(item)
                        else:
                            table_dict[device_name][dgp_name][cpg_name].update({priority: [item]})
                    else:
                        table_dict[device_name][dgp_name].update({cpg_name: {priority: [item]}})
                else:
                    table_dict[device_name].update({dgp_name: {cpg_name: {priority: [item]}}})
            else:
                table_dict.update({device_name: {dgp_name: {cpg_name: {priority: [item]}}}})

        # set table view

        start_index = 0
        arry = []
        for device, device_obj in table_dict.items():
            device_rowspan =0
            device_rowspan_flag = True
            device_start_index = 0

            for dgp, dgp_obj in device_obj.items():
                dgp_rowspan = 0
                dgp_rowspan_flag = True
                dgp_start_index = 0

                for cgp, cgp_obj in dgp_obj.items():
                    cgp_rowspan = 0
                    cgp_rowspan_flag = True
                    cgp_start_index = 0

                    for pri_name, pir_obj in cgp_obj.items():
                        pri_rowspan = 0
                        pri_rowspan_flag = True
                        pri_start_index = 0

                        for entry in pir_obj:
                            device_rowspan +=1
                            dgp_rowspan += 1
                            cgp_rowspan += 1
                            pri_rowspan += 1
                            data = {
                                "item_id": entry['item_id'],
                                "device": entry['device_name'],
                                "deviceNo": entry['device_id'],
                                'policyNo': entry['coll_policy_id'],
                                'cpGroup': entry['policy_group_name'],
                                'cpGroupNo': entry['policy_group_id'],
                                'device': entry['device_name'],
                                'deviceGroupNo': entry['device_group_id'],
                                'deviceGroup': entry['device_group_name'],
                                'priority': Tool.set_priority_mapping(entry['priority']),
                                'policy': '{}  {}'.format(entry['policy_name'], entry['exec_interval']),
                                'attr': {
                                    'device': {
                                        'rowspan': None
                                    },
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
                            if device_rowspan_flag:
                                device_start_index = start_index
                                device_rowspan_flag = False
                            if dgp_rowspan_flag:
                                dgp_start_index = start_index
                                dgp_rowspan_flag = False
                            if cgp_rowspan_flag:
                                cgp_start_index = start_index
                                cgp_rowspan_flag = False
                            if pri_rowspan_flag:
                                pri_start_index = start_index
                                pri_rowspan_flag = False

                            arry.append(data)
                            start_index += 1

                        arry[pri_start_index]['attr']['priority']['rowspan'] = pri_rowspan

                    arry[cgp_start_index]['attr']['cpGroup']['rowspan'] = cgp_rowspan

                arry[dgp_start_index]['attr']['deviceGroup']['rowspan'] = dgp_rowspan

            arry[device_start_index]['attr']['device']['rowspan'] = device_rowspan

        return arry