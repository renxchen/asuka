#!/usr/bin/env python
# coding=utf-8
"""

@author: necwang
@contact: necwang@cisco.com
@file: data_table_step3_views.py
@time: 2018/1/15 16:34
@desc:

"""

import traceback

from rest_framework import viewsets
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import Schedules, PolicysGroups


class DataTableCoulumnViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableCoulumnViewsSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        # device group id
        self.device_group_id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.device_group_name = views_helper.get_request_value(self.request, 'device_group_name', 'GET')

    @staticmethod
    def map_priority(value):
        """!@brief
        Match the priority， change the integer value into string value,
        0: 高, 1: 标准
        @param value: the integer value of priority
        @pre call when need to change priority
        @post return string priority
        @return priority: string priority
        """
        priority = ''
        if value == constants.NUMBER_ZERO:
            priority = constants.DATA_TABLE_PROORITY_0
        if value == constants.NUMBER_ONE:
            priority = constants.DATA_TABLE_PROORITY_1
        return priority

    def migrate_dic(self, data):
        dic = {}
        for i in data:
            policy_group_id = i['policy_group_id']
            schedule_id = i['schedule_id']
            priority = self.map_priority(i['priority'])
            key = str(schedule_id)
            dic[key] = priority
        return dic

    def get(self):
        """!@brief
        Get data for Step 3 when click [新规登陆]
        @return data: data for Step 3
        """
        try:
            data = []
            if self.device_group_id is not '':
                # get policy group ids base on device group id
                schedule_infos = Schedules.objects.filter(**{'device_group_id': self.device_group_id}).values(
                    'policy_group_id', 'schedule_id', 'priority')
                dic = self.migrate_dic(schedule_infos)
                if len(schedule_infos) > 0:
                    # device group rowspan
                    device_group_rowspan = 0
                    for per_schedule_info in schedule_infos:
                        policys_groups_infos = PolicysGroups.objects.filter(
                            **{'policy_group_id': per_schedule_info['policy_group_id']}).values('policy',
                                                                                                'policy_group__name')
                        device_group_rowspan += len(policys_groups_infos)
                    for per_schedule_info in schedule_infos:
                        count = 0
                        policys_groups_infos = PolicysGroups.objects.filter(
                            **{'policy_group_id': per_schedule_info['policy_group_id']}).values('policy',
                                                                                                'policy__name',
                                                                                                'policy__policy_type',
                                                                                                'policy_group__name',
                                                                                                'policy_group_id',
                                                                                                'policy__snmp_oid')
                        for policy_info in policys_groups_infos:
                            result_dict = {
                                'policyNo': '',
                                'groupNo': '',
                                'deviceGroup': self.device_group_name,
                                'cpGroup': '',
                                'policy': '',
                                'method': '',
                                'priority': '',
                                'attr': {
                                    'priority': {
                                        'rowspan': ''
                                    },
                                    'deviceGroup': {
                                        'rowspan': ''
                                    },
                                    'cpGroup': {
                                        'rowspan': ''
                                    }
                                }
                            }
                            count += 1
                            # collection policy group rowspan
                            cp_group_rowspan = 'None'
                            if count == 1:
                                cp_group_rowspan = len(policys_groups_infos)
                            # policy id
                            result_dict['policyNo'] = policy_info['policy']
                            # group id
                            result_dict['groupNo'] = self.device_group_id
                            # collection policy group name
                            result_dict['cpGroup'] = policy_info['policy_group__name']
                            # collection policy group id
                            result_dict['cpGroup_id'] = per_schedule_info['policy_group_id']
                            # collection policy name
                            result_dict['policy'] = policy_info['policy__name']
                            result_dict['priority'] = dic[str(per_schedule_info['schedule_id'])]
                            result_dict['schedule_id'] = per_schedule_info['schedule_id']
                            policy_type = 'CLI'
                            if int(policy_info['policy__policy_type']) == 1:
                                policy_type = 'SNMP'
                                result_dict['oid'] = policy_info['policy__snmp_oid']
                            result_dict['method'] = policy_type
                            if cp_group_rowspan is 'None':
                                device_group_rowspan = 'None'
                            result_dict['attr']['deviceGroup']['rowspan'] = device_group_rowspan
                            result_dict['attr']['cpGroup']['rowspan'] = cp_group_rowspan
                            result_dict['attr']['priority']['rowspan'] = cp_group_rowspan
                            data.append(result_dict)
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
                else:
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.DEVICE_GROUP_NOT_EXIST_IN_SCHEDULE
                        },
                    }
                    return api_return(data=data)
            else:
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.DEVICE_GROUP_NOT_EXIST
                    },
                }
                return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
