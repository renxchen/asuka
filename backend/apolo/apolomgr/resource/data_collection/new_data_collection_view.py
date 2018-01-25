#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: new_data_collection_view.py
@time: 2018/1/5 11:29
@desc:

'''
from django.db import transaction
from rest_framework import viewsets

from backend.apolo.models import Ostype, CollPolicyGroups, Groups, DevicesGroups, PolicysGroups, CollPolicyRuleTree, \
    Items, Schedules
from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.serializer.data_collection_serializer import CollPolicyGroupIDNameSerializer, \
    DeviceGroupIDNameSerializer, SchedulesAddSerializer, ItemsSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class NewDataCollectionViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(NewDataCollectionViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        #
        self.ostype_id = views_helper.get_request_value(self.request, "ostype_id", 'GET')

        # insert
        self.ostype = views_helper.get_request_value(self.request, "ostype_id", 'BODY')
        self.priority = views_helper.get_request_value(self.request, "priority", 'BODY')
        self.device_group_id = views_helper.get_request_value(self.request, "device_group_id", 'BODY')
        self.policy_group_id = views_helper.get_request_value(self.request, "policy_group_id", 'BODY')
        self.valid_period_type = views_helper.get_request_value(self.request, "valid_period_type", 'BODY')
        self.start_period_time = views_helper.get_request_value(self.request, "start_period_time", 'BODY')
        self.end_period_time = views_helper.get_request_value(self.request, "end_period_time", 'BODY')
        self.data_schedule_type = views_helper.get_request_value(self.request, "data_schedule_type", 'BODY')
        self.weeks = views_helper.get_request_value(self.request, "weeks", 'BODY')
        # self.schedule_start_time = views_helper.get_request_value(self.request, "schedule_start_time", 'BODY')
        # self.schedule_end_time = views_helper.get_request_value(self.request, "schedule_end_time", 'BODY')
        self.data_schedule_time = views_helper.get_request_value(self.request, "data_schedule_time", 'BODY')

    @staticmethod
    def __get_ostype__():

        ostype_queryset = Ostype.objects.all()
        serializer = OstypeSerializer(ostype_queryset, many=True)
        return serializer.data

    def __get_device_groups__(self):

        group_queryset = Groups.objects.filter(ostype=self.ostype_id)
        serializer = DeviceGroupIDNameSerializer(group_queryset, many=True)
        return serializer.data

    def __get_coll_policy_groups__(self):
        cp_group_queryset = CollPolicyGroups.objects.filter(ostypeid=self.ostype_id)
        serializer = CollPolicyGroupIDNameSerializer(cp_group_queryset, many=True)
        return serializer.data

    def get(self):
        # v1/api_new_data_collection/ new page init
        # v1/api_new_data_collection/?ostype_id=xx
        if self.ostype_id:
            # when Os type is selected
            cp_groups_dict = self.__get_coll_policy_groups__()
            device_groups_dict = self.__get_device_groups__()
            data = {
                'device_groups': device_groups_dict,
                'cp_groups': cp_groups_dict,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
        else:
            all_ostype_data = self.__get_ostype__()
            data = {
                'data': all_ostype_data,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }

        return api_return(data=data)

    def __insert_data_check__(self, devices, coll_policies):

        select_sql = 'select item_id,schedule_id from Items where'

        for i in range(len(devices)):
            device_id = devices[i]
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
            query_set = Schedules.objects.exclude(schedule_id__in=schedule_id_list).values('priority').distinct()
            priorityIsEqual = True
            for item in query_set:
                if self.priority == item['priority']:
                    priorityIsEqual = False

            return priorityIsEqual
        else:
            return True

    def __set_schedule_data__(self):

        # if self.weeks:
        #     week_time = ';'.join(self.weeks)
        # else:
        #     week_time = '1;2;3;4;5;6;7'

        # data_schedule_time = '{}@{}-{}'.format(week_time, self.schedule_start_time, self.schedule_end_time)
        schedule_recode_data = {
            'valid_period_type': self.valid_period_type,
            'data_schedule_type': self.data_schedule_type,
            'start_period_time': None,#self.start_period_time,
            'end_period_time': None, #self.end_period_time,
            'data_schedule_time': None,#self.data_schedule_time,
            'priority': self.priority,
            'status': constants.SCHEDULE_STATUS_DEFAULT,
            'policy_group': self.policy_group_id,
            'device_group': self.device_group_id,
            'ostype': self.ostype
        }
        return schedule_recode_data

    def __get_devices__(self):
        devices = DevicesGroups.objects.filter(group=self.device_group_id).values()
        devices_list = []
        for arry in devices:
            devices_list.append(arry['device_id'])
        return devices_list

    def __get_coll_policies__(self):

        query_set = PolicysGroups.objects.filter(policy_group=self.policy_group_id)
        policy_list = []
        for arry in query_set:
            print arry.policys_groups_id
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

    # desc: get tree_id and rule_id and rule_context of the policies
    # return value:
    # common policy_type
    # if the item is cli
    # coll_policy_id,tree_id,rule_id,rule__value_type,rule_key_str
    # else the item is snmp
    # coll_policy_id,snmp_oid of policy,value_type of policy
    @staticmethod
    def __get_items_context__(schedule_id, coll_policies):
        items_arry = []
        for arry in coll_policies:
            coll_policy_id = arry['coll_policy_id']
            policys_groups_id = arry['policys_groups_id']
            item_type = arry['policy_type']
            if item_type == constants.ITEM_TYPE_SNMP:
                print 'snmp:{}'.format(coll_policy_id)
                key_str = arry['snmp_oid']
                value_type = arry['value_type']
                data = {
                    'value_type': value_type,
                    'item_type': item_type,
                    'key_str': key_str,
                    'status': constants.ITEM_TABLE_STATUS_DEFAULT,
                    'last_exec_time': None,
                    'coll_policy': coll_policy_id,
                    'coll_policy_rule_tree_treeid':0,
                    'device': None,
                    'schedule': schedule_id,
                    'policys_groups':policys_groups_id
                }
                items_arry.append(data)
            if item_type == constants.ITEM_TYPE_CLI:
                print 'cli:{}'.format(coll_policy_id)
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
                        'policys_groups': policys_groups_id
                    }
                    items_arry.append(data)
        return items_arry

    def post(self):
        # ready
        # get device list
        devices_list = self.__get_devices__()
        # get coll_policies
        coll_policy_list = self.__get_coll_policies__()
        # data check
        if not self.__insert_data_check__(devices_list, coll_policy_list):
            data = {
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.POLICY_DEVICE_COMBINATION  # can not insert
                }
            }
            return api_return(data=data)
        else:
            try:
                # ready
                # get tree_id and rule_id of the collection policy tree
                schedule_data = self.__set_schedule_data__()
                serializer = SchedulesAddSerializer(data=schedule_data)
                with transaction.atomic():
                    # insert data into schedule table
                    if serializer.is_valid(raise_exception=BaseException):
                        serializer.save()
                        schedule_id = serializer.data['schedule_id']
                        item_list = self.__get_items_context__(schedule_id, coll_policy_list)
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

