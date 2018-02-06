#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_by_cp_view.py
@time: 2018/1/23 9:23
@desc:

'''
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.tool import Tool
from backend.apolo.models import CollPolicy
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.views_helper import api_return


class DataCollectionByCPViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataCollectionByCPViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    def get(self):
        coll_policy_id = views_helper.get_request_value(self.request, "policy_id", "GET")

        if not coll_policy_id:
            # load all coll_policy
            coll_policy_list = CollPolicy.objects.values('policy_id', 'name')
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
            coll_policy_id =3
            response_json_data = Tool.get_data_from_collection_server()
            arry = []
            for one_recoder in response_json_data['items']:
                if one_recoder['coll_policy_id'] == coll_policy_id:
                    policy_name = one_recoder['policy_name']
                    info = {
                        'deviceNo': one_recoder['device_id'],
                        'device': one_recoder['device_name'],
                        'policy': policy_name,
                        'policyNo': one_recoder['coll_policy_id'],
                        'status': Tool.set_cp_status_mapping(one_recoder['valid_status']),
                        'attr': {
                            'policy': {
                                'rowspan': None
                            }
                        }
                    }
                    arry.append(info)

            arry[0]['attr']['policy']['rowspan']= len(arry)
            data = {
                'data': arry,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
