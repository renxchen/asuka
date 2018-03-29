#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_by_cp_view.py
@time: 2018/1/23 9:23
@desc:

'''
from django.core.paginator import Paginator
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.models import CollPolicy
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.views_helper import api_return


class DataCollectionByCPViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataCollectionByCPViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')

    def get(self):
        # http://127.0.0.1:8000/v1/api_data_collection_policy/?policy_id=3&device_name=test
        # http://127.0.0.1:8000/v1/api_data_collection_policy/?page=1&rows=1&policy_id=3&device_name=test
        coll_policy_id = views_helper.get_request_value(self.request, "coll_policy_id", "GET")
        device_name = views_helper.get_request_value(self.request, "device", "GET")
        if not coll_policy_id:
            # load all coll_policy
            coll_policy_list = CollPolicy.objects.values('coll_policy_id', 'name', 'policy_type')
            arry = []
            for item in coll_policy_list:
                arry.append(item)
            data = {
                'policies': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        else:
            response_json_data = Tool.get_data_from_collection_server()
            arry = []
            for one_recoder in response_json_data:
                if device_name:
                    if device_name in one_recoder['device_name']:
                        isFilter = True
                    else:
                        isFilter = False
                else:
                    isFilter = True
                if int(one_recoder['coll_policy_id']) == int(coll_policy_id) and isFilter:
                    info = {
                        'deviceNo': one_recoder['device_id'],
                        'device': one_recoder['device_name'],
                        'status': Tool.set_cp_status_mapping(one_recoder['valid_status']),
                    }
                    arry.append(info)
            total_num = len(arry)
            paginator = Paginator(arry, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': contacts.object_list,
                'num_page': paginator.num_pages,
                'page_has_next': contacts.has_next(),
                'total_num': total_num,
                'current_page_num': contacts.number,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
