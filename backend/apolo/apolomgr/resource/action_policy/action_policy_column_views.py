#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: kimli
@contact: kimli@cisco.com
@file: action_policy_column_views.py
@time: 2018/2/12 12:34
@desc:

"""
import traceback
from rest_framework import viewsets
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import DataTable
import logging
from backend.apolo.apolomgr.resource.action_policy_table.data_table_step1_views import TableViewsSet
from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree


class ActionPolicyColumnViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(ActionPolicyColumnViewSet, self).__init__(**kwargs)
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
        self.table_id = views_helper.get_request_value(self.request, 'id', method)
        self.policy_id = views_helper.get_request_value(self.request, 'policy_id', method)

    def get(self):
        try:
            if self.table_id is not '':
                tvs = TableViewsSet(request=self.request)
                data_history = tvs.get_info_by_table_id(self.table_id)
                # get tree information
                pt = Policy_tree(self.policy_id)
                pt_data = pt.get_policy_tree()
                data = {
                    'data': {
                        'table_name': DataTable.objects.get(table_id=self.table_id).name,
                        'table_id': DataTable.objects.get(table_id=self.table_id).table_id,
                        'data_history': data_history,
                        'policy_tree': pt_data,
                    },
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                }
                return api_return(data=data)
            dt_query = DataTable.objects.all()
            dt = dt_query.values('table_id', 'name', 'coll_policy__name', 'descr', 'groups', 'tree', 'coll_policy')
            data_all = []
            for per_dt in dt:
                result = {
                    'name': per_dt['name'],
                    'table_id': per_dt['table_id'],
                    'group_id': per_dt['groups'],
                    'tree_id': per_dt['tree'],
                    'policy_name': per_dt['coll_policy__name'],
                    'policy_id': per_dt['coll_policy'],
                    'desc': per_dt['descr']
                }
                data_all.append(result)
            paginator = Paginator(data_all, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': {
                    'data': contacts.object_list,
                },
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                'page_range': list(paginator.page_range),
                'page_has_next': contacts.has_next(),
                'total_num': len(contacts.object_list),
                'current_page_num': contacts.number,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
