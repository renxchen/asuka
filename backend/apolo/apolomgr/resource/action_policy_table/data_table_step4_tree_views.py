#!/usr/bin/env python
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


class DataTableTreeViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableTreeViewsSet, self).__init__(**kwargs)
        self.request = request
        # collection policy id
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')

    def get(self):
        """
        Get the tree in left of action policy step 4
        API: http://127.0.0.1:1111/v1/api_data_table_tree/?id=2
        :return: tree
        """
        try:
            if self.id is not '':
                policy_tree = Policy_tree(self.id)
                # get policy tree
                policy_tree_dict = policy_tree.get_policy_tree()
                return api_return(data=policy_tree_dict)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)
