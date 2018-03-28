#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection.py
@time: 2018/2/28 12:49
@desc:

'''
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
        try:
            # check the device nums in the devices group and policy nums in policy group
            if len(devices_list) == 0:
                return False, constants.NO_DEVICE_IN_DEVICE_GROUP
            elif len(coll_policy_list) == 0 and policy_group_id > -1:
                return False, constants.NO_CP_IN_CP_GROUP
            else:
                data_check_res = True
                # if is not  all functions off
                if not policy_group_id == -1:
                    data_check_res = self.insert_data_check(devices_list, coll_policy_list)
                # data check
                if not data_check_res:
                    return False, constants.POLICY_DEVICE_COMBINATION
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
                return item_serializer.data
        except Exception as e:
            print e
            raise e

    # when device update
    def update_items(self):
        items_list = self.request_param['items']
        for obj in items_list:
            if obj['del_device_group']:
                self.__del_item_opt(obj)
            if obj['add_device_group']:
                self.__add_item_opt(obj)

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
            select_sql = 'select item_id,schedule_id from items where'
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

    def set_schedule_data(self, status=constants.SCHEDULE_STATUS_DEFAULT):
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


    def __add_item_opt(self, add_item_info):
        device_id = add_item_info['device_id']
        device_group_id_list = add_item_info['add_device_group']
        try:
            # select schedule_id and policy group id corresponding to these device group
            schedule_list = Schedules.objects.filter(device_group__in=device_group_id_list).values('schedule_id',
                                                                                                   'policy_group',
                                                                                                   'device_group')
            item_table_id_pair = []
            for schedule in schedule_list:
                if schedule['policy_group']:
                    # select all policies  corresponding to the policy group
                    policy_list = self.get_coll_policies(cp_group_id=schedule['policy_group'])
                    # add items
                    devices = [{"device_id": device_id, "device_group_id": schedule['device_group']}]
                    items_list = self.insert_new_items(devices, schedule['schedule_id'], policy_list)
                    for obj in items_list:
                        # create the pair of item_id and table_id
                        item_id = obj['item_id']
                        coll_policy_id = obj['coll_policy']
                        tree_id = obj['coll_policy_rule_tree_treeid']
                        device_group_id = obj['groups']
                        data_table_queryset = DataTable.objects.filter(coll_policy=coll_policy_id,
                                                            groups=device_group_id,
                                                            tree_id=tree_id).values()

                        for data_table in data_table_queryset:
                            item_table_id_pair.append({'item': item_id, 'table': data_table['table_id']})
                # insert the pair of item_id and table_id into data_table_items table
            serializer =DataTableItemsSerializer(data=item_table_id_pair, many=True)
            if serializer.is_valid(BaseException):
                serializer.save()
        except Exception as e:
            print e
            raise e



if __name__ == "__main__":
    data = {"items": [{
                     "device_id": 5,
                     "del_device_group": [5],
                     "add_device_group": []
                     }]
           }
    opt =DataCollectionOptCls(**data)
    opt.update_items()
