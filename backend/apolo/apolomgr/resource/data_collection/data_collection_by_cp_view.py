#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_by_cp_view.py
@time: 2018/1/23 9:23
@desc:

'''
from rest_framework import viewsets

from backend.apolo.models import CollPolicy
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.views_helper import api_return


class DataCollectionByCPViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataCollectionByCPViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    def get(self):
        coll_policy_id = views_helper.get_request_value(self.request, "coll_policy_id", "GET")

        if not coll_policy_id:
            # load all coll_policy
            coll_policy_list = CollPolicy.objects.values('coll_policy_id', 'name')
            arry = []
            for item in coll_policy_list:
                arry.append(item)
            data = {
                'devices': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        else:
            pass
