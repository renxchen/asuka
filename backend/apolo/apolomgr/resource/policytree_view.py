#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: policytree_view.py
@time: 2017/12/18 18:24
@desc:

'''
from rest_framework import viewsets
import json

from backend.apolo.apolomgr.resource.render import Render
from backend.apolo.tools.common import api_return


class PolicyTreeViewSet(viewsets.Viewset):

    def __init__(self, request, **kwargs):
        super(PolicyTreeViewSet, self).__init__(**kwargs)
        self.request = request

    def get(self):
        raw_data=''
        tree_json ={}
        tree_id=''

        if 'raw_data' in self.request.GET.keys():
            raw_data = self.request.GET['raw_data']
        if 'tree_json' in self.request.GET.keys():
            tree_json = json.loads(self.request.GET['tree_json'])
        if 'tree_id' in self.request.GET('tree_id'):
            tree_id = self.request.GET('tree_id')

        request_dict = {
            'data': raw_data,
            'tree': tree_json,
            'tree_id': tree_id
        }

        render = Render(**request_dict)
        html_data = render.render()
        return api_return(data=html_data)


    def post(self):
        policy_id=''
        tree_json = {}
        if 'tree_json' in self.request.GET.keys():
            tree_json = json.loads(self.request.GET['tree_json'])
        if 'policy_id' in self.request.GET('policy_id'):
            policy_id = self.request.GET('policy_id')



        print policy_id
        print tree_json

        pass

    def put(self):
        pass

    def delete(self):
        pass



