#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection.py
@time: 2018/2/28 12:49
@desc:

'''
from django.db import transaction

from apolo_server.processor.db_units.models import PolicysGroups, Items, Schedules, CollPolicyRuleTree
from backend.apolo.db_utils.db_until import *
from backend.apolo.models import DevicesGroups
from backend.apolo.serializer.data_collection_serializer import SchedulesAddSerializer, ItemsSerializer
from backend.apolo.tools import constants


class DataCollectionOptCls(object):
    def __init__(self, **request_param):
        self.request_param = request_param
        self.device_group_id = self.request_param['device_group_id']
        self.policy_group_id = self.request_param['policy_group_id']

    def insert_new_schedule_bk(self):
        # ready
        # get device list
        devices_list = self.__get_devices()
        # get coll_policies
        coll_policy_list = self.__get_coll_policies()
        # check the device nums in the devices group and policy nums in policy group
        if len(devices_list) == 0 or len(coll_policy_list) == 0:
            data = {
                constants.STATUS: {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.NO_ITEMS_IN_GROUP  # can not insert
                }
            }
            return data
        else:
            # data check
            if not self.__insert_data_check(devices_list, coll_policy_list):
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.POLICY_DEVICE_COMBINATION  # can not insert
                    }
                }
                return data
            else:
                # ready
                # get tree_id and rule_id of the collection policy tree
                schedule_data = self.set_schedule_data()
                serializer = SchedulesAddSerializer(data=schedule_data)
                # insert data into schedule table
                if serializer.is_valid(raise_exception=BaseException):
                    serializer.save()
                    schedule_id = serializer.data['schedule_id']
                    item_list = self.__get_items_context(schedule_id, coll_policy_list)
                    policy_device_combinations = []
                    for device_id in devices_list:
                        for item in item_list:
                            item['device'] = device_id
                            combination = item.copy()
                            policy_device_combinations.append(combination)

                    item_serializer = ItemsSerializer(data=policy_device_combinations, many=True)
                    if item_serializer.is_valid(raise_exception=BaseException):
                        item_serializer.save()
                        data = {
                            constants.STATUS: {
                                constants.STATUS: constants.TRUE,
                                constants.MESSAGE: constants.SUCCESS
                            }
                        }
                        return data

    def add_new_schedule_ready(self):
        devices_list = self.get_devices()
        # get coll_policies
        coll_policy_list = self.get_coll_policies()
        return devices_list, coll_policy_list

    def insert_new_schedule(self, devices_list, coll_policy_list):

        try:
            # check the device nums in the devices group and policy nums in policy group
            if len(devices_list) == 0 or len(coll_policy_list) == 0:
                return False, constants.NO_ITEMS_IN_GROUP
            else:
                # data check
                if not self.__insert_data_check(devices_list, coll_policy_list):
                    return False, constants.POLICY_DEVICE_COMBINATION
                else:
                    # ready
                    # get tree_id and rule_id of the collection policy tree
                    schedule_data = self.set_schedule_data()
                    serializer = SchedulesAddSerializer(data=schedule_data)
                    # insert data into schedule table
                    if serializer.is_valid(raise_exception=BaseException):
                        serializer.save()
                        schedule_id = serializer.data['schedule_id']
                        return True, schedule_id
        except Exception as e:
            print e
            raise e

    def insert_new_items(self, device_list, schedule_id, coll_policy_list):
        try:
            item_list = self.__get_items_context(schedule_id, coll_policy_list)
            policy_device_combinations = []
            for device in device_list:
                for item in item_list:
                    item['device'] = device['device_id']
                    item['groups'] = device['device_group_id']
                    combination = item.copy()
                    policy_device_combinations.append(combination)

            item_serializer = ItemsSerializer(data=policy_device_combinations, many=True)
            if item_serializer.is_valid(raise_exception=BaseException):
                item_serializer.save()
                return True
        except Exception as e:
            print e
            raise e

    def get_devices(self):
        try:
            devices = DevicesGroups.objects.filter(group=self.device_group_id).values()
            devices_list = []
            for arry in devices:
                data = {
                    'device_id': arry['device_id'],
                    'device_group_id': self.device_group_id,
                }
                devices_list.append(data)
            return devices_list
        except Exception as e:
            print e
            raise e

    def get_coll_policies(self):
        try:
            query_set = PolicysGroups.objects.filter(policy_group=self.policy_group_id)
            policy_list = []
            for arry in query_set:
                data = {
                    'policys_groups_id': arry.policys_groups_id,
                    'coll_policy_id': arry.policy.coll_policy_id,
                    'item_type': arry.policy.policy_type,
                    'snmp_oid': arry.policy.snmp_oid,
                    'value_type': arry.policy.value_type,
                    'policy_type': arry.policy.policy_type
                }
                policy_list.append(data)
            return policy_list
        except Exception as e:
            print e
            raise e

    def __insert_data_check(self, devices, coll_policies):

        try:
            select_sql = 'select item_id,schedule_id from Items where'
            for i in range(len(devices)):
                device_id = devices[i]['device_id']
                for j in range(len(coll_policies)):
                    coll_policy_id = coll_policies[j]['coll_policy_id']
                    if i == len(devices) - 1 and j == len(coll_policies) - 1:
                        select_sql += ' (coll_policy_id = {} and device_id = {})'.format(coll_policy_id, device_id)
                    else:
                        select_sql += ' (coll_policy_id = {} and device_id = {}) or '.format(coll_policy_id, device_id)
            query_list = list(Items.objects.raw(select_sql))
            schedule_id_dict = {}
            if len(query_list):
                for sid in query_list:
                    if not schedule_id_dict.has_key(sid.schedule_id):
                        schedule_id_dict[sid.schedule_id] = 1
                schedule_id_list = schedule_id_dict.keys()
                query_set = Schedules.objects.filter(schedule_id__in=schedule_id_list).values('priority').distinct()
                priorityIsEqual = True
                for item in query_set:
                    if int(self.request_param['priority']) == int(item['priority']):
                        priorityIsEqual = False
                return priorityIsEqual
            else:
                return True
        except Exception as e:
            print e
            raise e

    def set_schedule_data(self):
        if self.request_param['data_schedule_time'] == '':
            self.request_param['data_schedule_time'] = None
        if self.request_param['start_period_time'] == '':
            self.request_param['start_period_time'] = None
        if self.request_param['end_period_time'] == '':
            self.request_param['end_period_time'] = None

        schedule_recode_data = {
            'valid_period_type': self.request_param['valid_period_type'],
            'data_schedule_type': self.request_param['data_schedule_type'],
            'start_period_time': self.request_param['start_period_time'],
            'end_period_time': self.request_param['end_period_time'],
            'data_schedule_time': self.request_param['data_schedule_time'],
            'priority': self.request_param['priority'],
            'status': constants.SCHEDULE_STATUS_DEFAULT,
            'policy_group': self.request_param['policy_group_id'],
            'device_group': self.request_param['device_group_id'],
            'ostype': self.request_param['ostype']

        }
        return schedule_recode_data

    @staticmethod
    def __get_items_context(schedule_id, coll_policies):
        try:
            items_arry = []
            for arry in coll_policies:
                coll_policy_id = arry['coll_policy_id']
                policys_groups_id = arry['policys_groups_id']
                item_type = arry['policy_type']
                if item_type == constants.ITEM_TYPE_SNMP:
                    key_str = arry['snmp_oid']
                    value_type = arry['value_type']
                    data = {
                        'value_type': value_type,
                        'item_type': item_type,
                        'key_str': key_str,
                        'status': constants.ITEM_TABLE_STATUS_DEFAULT,
                        'last_exec_time': None,
                        'coll_policy': coll_policy_id,
                        'coll_policy_rule_tree_treeid': None,
                        'device': None,
                        'schedule': schedule_id,
                        'policys_groups': policys_groups_id,
                        'enable_status': 1,
                        'groups': None
                    }
                    items_arry.append(data)
                if item_type == constants.ITEM_TYPE_CLI:

                    leaf_query_set = CollPolicyRuleTree.objects.filter(coll_policy=coll_policy_id,
                                                                       is_leaf=constants.LEAF_NODE_MARK)
                    for leaf in leaf_query_set:
                        key_str = leaf.rule.key_str
                        value_type = leaf.rule.value_type
                        tree_id = leaf.treeid
                        data = {
                            'value_type': value_type,
                            'item_type': item_type,
                            'key_str': key_str,
                            'status': constants.ITEM_TABLE_STATUS_DEFAULT,
                            'last_exec_time': None,
                            'coll_policy': coll_policy_id,
                            'coll_policy_rule_tree_treeid': tree_id,
                            'device': None,
                            'schedule': schedule_id,
                            'policys_groups': policys_groups_id,
                            'enable_status': 1,
                            'groups': None
                        }
                        items_arry.append(data)
            return items_arry
        except Exception as e:
            print e
            raise e