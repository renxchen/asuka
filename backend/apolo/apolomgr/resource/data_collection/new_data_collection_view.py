#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: new_data_collection_view.py
@time: 2018/1/5
@desc:

"""
import traceback

from django.db import transaction
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.data_collection.data_collection import DataCollectionOptCls
from backend.apolo.models import Ostype, CollPolicyGroups, Groups, CollPolicyRuleTree
from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.serializer.data_collection_serializer import CollPolicyGroupIDNameSerializer, \
    DeviceGroupIDNameSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class NewDataCollectionViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(NewDataCollectionViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
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
        self.data_schedule_time = views_helper.get_request_value(self.request, "data_schedule_time", 'BODY')

    @staticmethod
    def __get_ostype():
        """!@brief
        get ostype list
        @author Gin Chen
        @date 2018/1/5
        """
        ostype_queryset = Ostype.objects.all()
        serializer = OstypeSerializer(ostype_queryset, many=True)
        return serializer.data

    def __get_device_groups(self):
        """!@brief
        get device group list by ostype id
        @author Gin Chen
        @date 2018/1/5
        """
        group_queryset = Groups.objects.filter(ostype=self.ostype_id)
        serializer = DeviceGroupIDNameSerializer(group_queryset, many=True)
        return serializer.data

    def __get_coll_policy_groups(self):
        """!@brief
        get collection policy group list by ostype id
        @author Gin Chen
        @date 2018/1/5
        """
        cp_group_queryset = CollPolicyGroups.objects.filter(ostypeid=self.ostype_id)
        serializer = CollPolicyGroupIDNameSerializer(cp_group_queryset, many=True)
        return serializer.data

    def get(self):
        """!@brief
        when jump to 'add a new schedule page',init ostype ,policy group, device group list
        @param
        @pre
        @post
        @return ostype list,policy group list,
        @author Gin Chen
        @date 2018/1/5
        """
        if self.ostype_id:
            # when Os type is selected
            cp_groups_dict = self.__get_coll_policy_groups()
            device_groups_dict = self.__get_device_groups()
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
            all_ostype_data = self.__get_ostype()
            data = {
                'data': all_ostype_data,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }

        return api_return(data=data)

    def post(self):
        """!@brief
        add one schedule into schedule table,and many items into item table
        @author Gin Chen
        @date 2018/1/5
        """
        try:
            with transaction.atomic():
                param_dict = self.__set_request_param()
                opt = DataCollectionOptCls(**param_dict)
                # ready
                devices_list, coll_policy_list = opt.add_new_schedule_ready()
                # check whether the tree of cp is null or not
                for cp_dict in coll_policy_list:
                    cp_id = cp_dict['coll_policy_id']
                    if cp_dict['item_type'] == constants.ITEM_TYPE_CLI:
                        cp_leaf_nodes = CollPolicyRuleTree.objects.filter(coll_policy=cp_id,
                                                                          is_leaf=constants.LEAF_NODE_MARK)
                        if len(cp_leaf_nodes) == 0:
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.NULL_TREE_IN_CP
                                }
                            }
                            return api_return(data=data)
                # insert schedule
                res = opt.insert_new_schedule(devices_list, coll_policy_list)
                if res[0]:
                    # create item by schedule
                    opt.insert_new_items(devices_list, res[1], coll_policy_list)
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                else:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: res[1]
                        }
                    }
                return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def __set_request_param(self):
        """!@brief
        set param from request data
        @author Gin Chen
        @date 2018/1/5
        """
        param_dict = {
            "ostype": self.ostype,
            "priority": self.priority,
            "device_group_id": self.device_group_id,
            "policy_group_id": self.policy_group_id,
            "valid_period_type": self.valid_period_type,
            "start_period_time": self.start_period_time,
            "end_period_time": self.end_period_time,
            "data_schedule_type": self.data_schedule_type,
            "weeks": self.weeks,
            "data_schedule_time": self.data_schedule_time
        }
        return param_dict
