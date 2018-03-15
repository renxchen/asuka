#!/usr/bin/env python
# coding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: data_table_step3_views.py
@time: 2018/1/15 16:34
@desc:

"""

import traceback

from rest_framework import viewsets
from django.utils.translation import gettext
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import Schedules, PolicysGroups, CollPolicy


class DataTableCoulumnViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableCoulumnViewsSet, self).__init__(**kwargs)
        self.request = request
        # device group id
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.device_group_name = views_helper.get_request_value(self.request, 'device_group_name', 'GET')

    def get(self):
        """!@brief
        Get data for Step 3 when click [新规登陆]
        @return data: data for Step 3
        """
        try:
            data = []
            if self.id is not '':
                # get policy group ids base on device group id
                policy_group_ids = Schedules.objects.filter(**{'device_group_id': self.id}).values_list(
                    'policy_group_id')
                # device group rowspan
                device_group_rowspan = 0
                for per_policy_group_id in policy_group_ids:
                    policy_infos = PolicysGroups.objects.filter(
                        **{'policy_group_id': per_policy_group_id[0]}).values('policy', 'policy_group__name')
                    device_group_rowspan += len(policy_infos)
                if len(policy_group_ids) > 0:
                    for per_policy_group_id in policy_group_ids:
                        count = 0
                        policy_infos = PolicysGroups.objects.filter(
                            **{'policy_group_id': per_policy_group_id[0]}).values('policy', 'policy_group__name')
                        for policy_info in policy_infos:
                            count += 1
                            # collection policy group rowspan
                            cp_group_rowspan = 'None'
                            if count == 1:
                                cp_group_rowspan = len(policy_infos)
                            result_dict = {
                                'policyNo': '',
                                'groupNo': '',
                                'deviceGroup': self.device_group_name,
                                'cpGroup': '',
                                'policy': '',
                                'method': '',
                                'attr': {
                                    'deviceGroup': {
                                        'rowspan': ''
                                    },
                                    'cpGroup': {
                                        'rowspan': ''
                                    }
                                }
                            }
                            collection_policy_name = CollPolicy.objects.filter(
                                **{'coll_policy_id': policy_info['policy']}).values('name', 'policy_type')
                            # policy id
                            result_dict['policyNo'] = policy_info['policy']
                            # group id
                            result_dict['groupNo'] = self.id
                            # collection policy group name
                            result_dict['cpGroup'] = policy_info['policy_group__name']
                            # collection policy name
                            result_dict['policy'] = collection_policy_name[0]['name']
                            policy_type = 'CLI'
                            if int(collection_policy_name[0]['policy_type']) == 0:
                                policy_type = 'SNMP'
                            result_dict['method'] = policy_type
                            if cp_group_rowspan is 'None':
                                device_group_rowspan = 'None'
                            result_dict['attr']['deviceGroup']['rowspan'] = device_group_rowspan
                            result_dict['attr']['cpGroup']['rowspan'] = cp_group_rowspan
                            data.append(result_dict)
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
