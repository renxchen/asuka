#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: necwang
@contact: necwang@cisco.com
@file: action_policy_column_verify.py
@time: 2018/2/12 12:34
@desc:

"""
import traceback
import importlib
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import Triggers, TriggerDetail, DataTableItems, DataTable
from django.db import transaction
from backend.apolo.serializer.action_policy_serializer import TriggerSerializer, ActionsSerializer, \
    TriggerDetailSerializer
import time
import simplejson as json
import logging
from backend.apolo.apolomgr.resource.action_policy_table.data_table_step1_views import TableViewsSet
from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree


class ActionPolicyColumnVerifyViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(ActionPolicyColumnVerifyViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.logger = logging.getLogger("apolo.log")
        method = 'GET'
        if request.method.lower() == 'get' or request.method.lower() == 'delete':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.table_id_A = views_helper.get_request_value(self.request, 'id_A', method)
        self.table_id_B = views_helper.get_request_value(self.request, 'id_B', method)

    def get(self):
        """!@brief
        When select column2 after choosing column1 in 新规页面, column1 and column2 should be same with below 3 points:
        1.the same device group
        2.the same schedule_id(data_table_item-->item-->schedule)
        3.the same policy execute inteval(data_table_item-->item-->policys_groups)
        @post return verify result
        @return data: return verify result
        """
        try:
            if self.table_id_A is not '' and self.table_id_B is not '':
                # table_a = DataTable.objects.filter(table_id=self.table_id_A).values('groups', 'coll_policy__value_type',
                #                                                                     'coll_policy__policy_type')
                table_a_str = ''
                table_b_str = ''
                table_a = DataTableItems.objects.filter(table_id=self.table_id_A).values('table__groups',
                                                                                         'item__schedule',
                                                                                         'item__policys_groups')
                if table_a:
                    table_a_str = str(table_a[0]['table__groups']) + '_' + str(
                        table_a[0]['item__schedule']) + '_' + str(
                        table_a[0]['item__policys_groups'])
                # table_b = DataTable.objects.filter(table_id=self.table_id_B).values('groups', 'coll_policy__value_type',
                #                                                                     'coll_policy__policy_type')
                table_b = DataTableItems.objects.filter(table_id=self.table_id_B).values('table__groups',
                                                                                         'item__schedule',
                                                                                         'item__policys_groups')
                if table_b:
                    table_b_str = str(table_b[0]['table__groups']) + '_' + str(
                        table_b[0]['item__schedule']) + '_' + str(
                        table_b[0]['item__policys_groups'])
                if table_a_str == table_b_str:
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        },
                    }
                    return api_return(data=data)
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.COLUMN_A_COLUMN_B_VERIFY_FAILED
                    },
                }
                return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
