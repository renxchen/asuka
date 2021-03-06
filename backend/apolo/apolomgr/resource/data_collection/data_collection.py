#!/usr/bin/env python

'''

@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: data_collection.py
@time: 2018/2/28 12:49
@desc:

'''


import operator
from django.db import transaction
from django.db.models import Q

from backend.apolo.db_utils.db_until import *
from backend.apolo.models import DevicesGroups, PolicysGroups, Items, Schedules, CollPolicyRuleTree, DataTableItems, \
    DataTable
from backend.apolo.serializer.data_collection_serializer import SchedulesAddSerializer, ItemsSerializer, \
    DataTableHistoryItemsSerializer, DataTableItemsSerializer
from backend.apolo.tools import constants


class DataCollectionOptCls(object):
    def __init__(self, **request_param):
        self.request_param = request_param

    def add_new_schedule_ready(self):
        devices_list = self.get_devices()
        # get coll_policies
        coll_policy_list = self.get_coll_policies()
        return devices_list, coll_policy_list

    # if policy_group_id = -1 ,set all functions off
    def insert_new_schedule(self, devices_list, coll_policy_list):
        policy_group_id = int(self.request_param['policy_group_id'])
        device_group_id = int(self.request_param['device_group_id'])
        try:
            # check the device nums in the devices group and policy nums in policy group
            if len(devices_list) == 0:
                return False, constants.NO_DEVICE_IN_DEVICE_GROUP
            elif len(coll_policy_list) == 0 and policy_group_id > -1:
                return False, constants.NO_CP_IN_CP_GROUP
            else:

                # if it is not  all functions off
                if not policy_group_id == -1:
                    data_check_res = self.insert_data_check(devices_list, coll_policy_list)
                else:
                    # do function all check
                    data_check_res = self.all_function_off_check(device_group_id)
                # data check
                if not data_check_res[0]:
                    return False, data_check_res[1]
                else:
                    # ready
                    # all function off
                    if policy_group_id == -1:
                        self.update_all_function_off_status(0)
                        schedule_data = self.set_schedule_data(status=0)
                    else:
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

    def insert_new_items(self, d_list, schedule_id, coll_policy_list):
        try:
            item_list = self.__get_items_context(schedule_id, coll_policy_list)
            policy_device_combinations = []
            for device in d_list:
                for one_item in item_list:
                    one_item['device'] = device['device_id']
                    one_item['groups'] = device['device_group_id']
                    combination = one_item.copy()
                    policy_device_combinations.append(combination)

            item_serializer = ItemsSerializer(data=policy_device_combinations, many=True)
            if item_serializer.is_valid(raise_exception=BaseException):
                item_serializer.save()
                return item_serializer.data
        except Exception as e:
            print e
            raise e

    # all function check
    @staticmethod
    def all_function_off_check(device_group_id):
        device_group_count = len(Schedules.objects.filter(device_group=device_group_id).values())
        all_function_is_have = len(Schedules.objects.filter(device_group=device_group_id, policy_group=None, status=0))
        if device_group_count ==0:
            return False, constants.DEVICE_GROUP_NOT_IN_SCHEDULE
        if all_function_is_have > 0:
            return False, constants.DEVICE_GROUP_IS_ALL_FUNCTION_ALL
        return True, constants.SUCCESS


    # when device update
    def update_items_bk(self):
        items_list = self.request_param['items']
        for obj in items_list:
            if obj['del_device_group']:
                self.__del_item_opt(obj)
            if obj['add_device_group']:
                self.__add_item_opt(obj)

    def update_items(self):
        items_list = self.request_param['items']
        add_item_list = []
        for obj in items_list:
            if obj['del_device_group']:
                self.__del_item_opt(obj)
            if obj['add_device_group']:
                add_item_list.append(obj)
        if len(add_item_list) > 0:
            self.__add_item_opt(add_item_list)

    # when set off all policies  by device group,
    # update status =0 of schedule table by device_group_id
    def update_all_function_off_status(self, status):
        device_group_id = int(self.request_param['device_group_id'])
        try:
            Schedules.objects.filter(device_group=device_group_id).update(status=status)
        except Exception as e:
            raise e

    def get_devices(self):
        device_group_id = int(self.request_param['device_group_id'])
        try:
            devices = DevicesGroups.objects.filter(group=device_group_id).values()
            devices_list = []
            for arry in devices:
                data = {
                    'device_id': arry['device_id'],
                    'device_group_id': device_group_id,
                }
                devices_list.append(data)
            return devices_list
        except Exception as e:
            print e
            raise e

    def get_coll_policies(self, cp_group_id=None):
        if not cp_group_id:
            policy_group_id = int(self.request_param['policy_group_id'])
        else:
            policy_group_id = cp_group_id
        try:
            query_set = PolicysGroups.objects.filter(policy_group=policy_group_id)
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

    def insert_data_check(self, devices, coll_policies):

        try:
            q_arry=[]
            for i in range(len(devices)):
                device_id = devices[i]['device_id']
                for j in range(len(coll_policies)):
                    coll_policy_id = coll_policies[j]['coll_policy_id']
                    q_arry.append(Q(coll_policy=coll_policy_id, device=device_id))
            query_list = Items.objects.filter(reduce(operator.or_, q_arry)).values()
            schedule_id_dict = {}
            if len(query_list):
                for sid in query_list:
                    if not schedule_id_dict.has_key(sid['schedule_id']):
                        schedule_id_dict[sid['schedule_id']] = 1
                schedule_id_list = schedule_id_dict.keys()
                query_set = Schedules.objects.filter(schedule_id__in=schedule_id_list).values('priority').distinct()
                priorityIsEqual = True
                for item in query_set:
                    if int(self.request_param['priority']) == int(item['priority']):
                        priorityIsEqual = False
                        break
                if priorityIsEqual:
                    return True, constants.SUCCESS
                else:
                    return False, constants.POLICY_DEVICE_COMBINATION
            else:
                return True, constants.SUCCESS
        except Exception as e:
            print e
            raise e

    def set_schedule_data(self, status=constants.SCHEDULE_STATUS_DEFAULT, update_flag=False):
        policy_group_id = int(self.request_param['policy_group_id'])
        if self.request_param['data_schedule_time'] == '':
            self.request_param['data_schedule_time'] = None
        if self.request_param['start_period_time'] == '':
            self.request_param['start_period_time'] = None
        if self.request_param['end_period_time'] == '':
            self.request_param['end_period_time'] = None
        if policy_group_id == -1:
            policy_group = None
        else:
            policy_group = policy_group_id
        if not update_flag:
            is_all_function_off = len(Schedules.objects.filter(device_group=int(self.request_param['device_group_id']),
                                                           policy_group=None))
            # when add a new schedule ,if the device group has been all function off,the schedule status=0
            if is_all_function_off >0:
                status = 0
        schedule_recode_data = {
            'valid_period_type': self.request_param['valid_period_type'],
            'data_schedule_type': self.request_param['data_schedule_type'],
            'start_period_time': self.request_param['start_period_time'],
            'end_period_time': self.request_param['end_period_time'],
            'data_schedule_time': self.request_param['data_schedule_time'],
            'priority': self.request_param['priority'],
            'status': status,  # constants.SCHEDULE_STATUS_DEFAULT,
            'policy_group': policy_group,  # self.request_param['policy_group_id'],
            'device_group': self.request_param['device_group_id'],
            'ostype': self.request_param['ostype']

        }
        return schedule_recode_data

    @staticmethod
    def __get_items_context(schedule_id, coll_policies):
        try:
            items_arry = []
            cli_policy = dict()
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
                    if cli_policy.has_key(coll_policy_id):
                        cli_policy[coll_policy_id].append(arry)
                    else:
                        cli_policy.update({coll_policy_id: [arry]})

            leaf_query_set = CollPolicyRuleTree.objects.filter(coll_policy__in=cli_policy.keys(),
                                                               is_leaf=constants.LEAF_NODE_MARK)
            for leaf in leaf_query_set:
                key_str = leaf.rule.key_str
                value_type = leaf.rule.value_type
                tree_id = leaf.treeid
                data = {
                    'value_type': value_type,
                    'item_type': None,
                    'key_str': key_str,
                    'status': constants.ITEM_TABLE_STATUS_DEFAULT,
                    'last_exec_time': None,
                    'coll_policy': leaf.coll_policy_id,
                    'coll_policy_rule_tree_treeid': tree_id,
                    'device': None,
                    'schedule': schedule_id,
                    'policys_groups': None,
                    'enable_status': 1,
                    'groups': None
                }
                for t in cli_policy[leaf.coll_policy_id]:
                    data['policys_groups'] = t['policys_groups_id']
                    data['item_type'] = t['policy_type']
                    items_arry.append(data)
            return items_arry
        except Exception as e:
            print e
            raise e

    @staticmethod
    def __del_item_opt(del_item_info):
        device_id = del_item_info['device_id']
        device_group_id_list = del_item_info['del_device_group']

        try:
            del_item_queryset = Items.objects.filter(device=device_id, groups__in=device_group_id_list)
            item_id_list = del_item_queryset.values("item_id")
            arry = []
            for item_id in item_id_list:
                arry.append(item_id['item_id'])
                # update enable_status = 0
            del_item_queryset.update(enable_status=0)
            # query item_id and table_id pair from data_table_items table

            item_table_pair_queryset = DataTableItems.objects.filter(item__in=arry)
            buff_dict = list(item_table_pair_queryset.values('table', 'item'))
            serializer = DataTableHistoryItemsSerializer(data=buff_dict, many=True)
            if serializer.is_valid(BaseException):
                # back up the item_id table_id pair into data_table_history_items table
                serializer.save()
                # del item_id table_id recoder from data_table_items
                item_table_pair_queryset.delete()
        except Exception as e:
            print e
            raise e

    def __add_item_opt(self, add_item_info_list):

        # get all device_group_id_list from item list
        # {device_id: [device_group_id]}
        try:
            device_info_dict = dict()
            all_device_group_list = []
            for info in add_item_info_list:
                device_id = info['device_id']
                device_group_id_list = info['add_device_group']
                device_info_dict.update({device_id: device_group_id_list})
                all_device_group_list.extend(device_group_id_list)

                # get all device_group_list
            all_device_group_list = list(set(all_device_group_list))
            # get all schedule id by all_device_group_id_list
            all_schedule_list = Schedules.objects.filter(device_group__in=all_device_group_list).values('schedule_id',
                                                                                                        'policy_group',
                                                                                                        'device_group')

            if len(all_schedule_list) > 0:
                # get all cp group infos and all cp infos
                all_cp_group_list = []
                # device group
                dgp_schedule_pair_dict = dict()
                for schedule_info in all_schedule_list:
                    cp_gp_id = schedule_info['policy_group']
                    dgp_id = schedule_info['device_group']
                    all_cp_group_list.append(cp_gp_id)
                    if dgp_schedule_pair_dict.has_key(dgp_id):
                        dgp_schedule_pair_dict[dgp_id].append(schedule_info)
                    else:
                        dgp_schedule_pair_dict.update({dgp_id: [schedule_info]})

                all_cp_group_list = list(set(all_cp_group_list))
                all_cp_group_info_dict = dict()
                policy_list = []

                query_set = PolicysGroups.objects.filter(policy_group__in=all_cp_group_list)

                for arry in query_set:
                    data = {
                        'policy_group_id': arry.policy_group_id,
                        'policys_groups_id': arry.policys_groups_id,
                        'coll_policy_id': arry.policy.coll_policy_id,
                        'item_type': arry.policy.policy_type,
                        'snmp_oid': arry.policy.snmp_oid,
                        'value_type': arry.policy.value_type,
                        'policy_type': arry.policy.policy_type
                    }
                    policy_list.append(data)
                    if all_cp_group_info_dict.has_key(data['policy_group_id']):
                        all_cp_group_info_dict[data['policy_group_id']].append(data)
                    else:
                        all_cp_group_info_dict.update({data['policy_group_id']: [data]})

                        # get all item info
                        # {policy_id:[{item_info}]
                all_item_info_dict = dict()
                all_item_list = self.__get_items_context(schedule_id='', coll_policies=policy_list)
                for item_info in all_item_list:
                    policy_id = item_info['coll_policy']
                    if all_item_info_dict.has_key(policy_id):
                        all_item_info_dict[policy_id].append(item_info)
                    else:
                        all_item_info_dict.update({policy_id: [item_info]})

                # clean data
                all_insert_infos = []

                for device_id, dpg_list in device_info_dict.items():
                    for dgp_id in dpg_list:
                        for schedule in dgp_schedule_pair_dict[dgp_id]:
                            cp_gp_id = schedule['policy_group']
                            cp_list = all_cp_group_info_dict[cp_gp_id]
                            for cp in cp_list:
                                cp_id = cp['coll_policy_id']
                                # there is no tree node in the cp so there is no item
                                item_data = all_item_info_dict[cp_id]
                                for data in item_data:
                                    data['device'] = device_id
                                    data['groups'] = dgp_id
                                    data['schedule'] = schedule['schedule_id']
                                    all_insert_infos.append(data.copy())

                item_serializer = ItemsSerializer(data=all_insert_infos, many=True)
                new_item_list = []
                item_table_id_pair = []
                if item_serializer.is_valid(raise_exception=BaseException):
                    item_serializer.save()
                    new_item_list = item_serializer.data

                q_list = []
                pair_dict = dict()
                for obj in new_item_list:
                    # create the pair of item_id and table_id
                    item_id = obj['item_id']
                    coll_policy_id = obj['coll_policy']
                    tree_id = obj['coll_policy_rule_tree_treeid']
                    device_group_id = obj['groups']
                    q_list.append(Q(coll_policy=coll_policy_id, groups=device_group_id, tree_id=tree_id))
                    if tree_id is None:
                        tree_id = 0
                    id_key = '{}_{}_{}'.format(coll_policy_id, tree_id, device_group_id)
                    if pair_dict.has_key(id_key):
                        pair_dict[id_key].append(item_id)
                    else:
                        pair_dict.update({id_key: [item_id]})

                data_table_list = DataTable.objects.filter(reduce(operator.or_, q_list)).values()
                for obj in data_table_list:
                    t_id = obj['tree_id']
                    c_id = obj['coll_policy_id']
                    d_id = obj['groups_id']
                    if t_id is None:
                        t_id = 0
                    find_key = '{}_{}_{}'.format(c_id, t_id, d_id)
                    if pair_dict.has_key(find_key):
                        for iid in pair_dict[find_key]:
                            item_table_id_pair.append({'item': iid, 'table': obj['table_id']})

                serializer = DataTableItemsSerializer(data=item_table_id_pair, many=True)
                if serializer.is_valid(BaseException):
                    serializer.save()
        except Exception as e:
            print e
            raise e


if __name__ == "__main__":

    try:
        with transaction.atomic():
            arry = []
            device_list = DevicesGroups.objects.filter(group=10).values('device', 'group')
            for item in device_list:
                arry.append({'device_id': item['device'], 'add_device_group': [14, 13], 'del_device_group': []})

            opt = DataCollectionOptCls(**{"items": arry})
            opt.update_items()
    except Exception as e:
        transaction.rollback()
        print e