#!/usr/bin/env python
# coding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: data_table_step4_tree_views.py
@time: 2018/1/15 16:34
@desc:

"""

import traceback

from rest_framework import viewsets
from django.utils.translation import gettext
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import views_helper
from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree
from backend.apolo.tools import constants


class DataTableTreeViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableTreeViewsSet, self).__init__(**kwargs)
        self.request = request
        # collection policy id
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')

    def get(self):
        """!@brief
        Get data in left for Step 4 when click [新规登陆]
        Get the tree for left in step 4
        @return data: data for left in step 4
        """
        try:
            if self.id is not '':
                policy_tree = Policy_tree(self.id)
                # get policy tree
                policy_tree_dict = policy_tree.get_policy_tree()
                return api_return(data=policy_tree_dict)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
