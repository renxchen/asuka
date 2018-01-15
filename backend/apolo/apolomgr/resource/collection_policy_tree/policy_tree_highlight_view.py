#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''

@author: kimli
@contact: kimli@cisco.com
@file: policy_tree_highlight_view.py
@time: 2017/12/18 18:24
@desc:

'''
import json
import traceback

from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.render import Render
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class PolicyTreeHighLightViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(PolicyTreeHighLightViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.raw_data = views_helper.get_request_value(self.request, 'raw_data', 'BODY')
        self.tree_id = views_helper.get_request_value(self.request, 'tree_id', 'BODY')
        self.tree = views_helper.get_request_value(self.request, 'tree', 'BODY')

    def post(self):
        request_dict = {
            'data': self.raw_data,
            'tree': self.tree,
            'tree_id': self.tree_id
        }
        try:
            render = Render(**request_dict)
            html_data = render.render()
            f = open(r'C:\Users\yangyuan\Desktop\D2\apolo\ntt W\text1.html', 'w')
            f.write(html_data)
            f.close()
            data = {
                'data': html_data,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)
