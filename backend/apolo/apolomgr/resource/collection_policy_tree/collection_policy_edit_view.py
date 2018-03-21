#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: collection_policy_edit_view.py
@time: 2018/1/18 18:20
@desc:

'''
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.models import CollPolicy, PolicysGroups
from backend.apolo.serializer.collection_policy_serializer import CollPolicyEditSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class CollectionPolicyEditViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollectionPolicyEditViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')


    # init collection policy edit page
    def get(self):
        # v1/api_collection_policy_edit_page/?coll_policy_id=1
        coll_policy_id = views_helper.get_request_value(self.request, "coll_policy_id", "GET")
        obj = CollPolicy.objects.get(coll_policy_id=coll_policy_id)
        is_used = False
        if not Tool.get_policy_status(coll_policy_id):
            is_used = True
        is_not_in_group = True
        if len(PolicysGroups.objects.filter(policy=coll_policy_id)) > 0:
            is_not_in_group = False
        column_status={
            'name': True,
            'desc': True,
            'ostype': is_not_in_group,
            'cli_command': is_used
        }
        serializer = CollPolicyEditSerializer(obj)
        data = {
            'data': {
                'policy_detail': serializer.data,
                'verify_result': column_status
            },
            'new_token': self.new_token,
            constants.STATUS: {
                constants.STATUS: constants.TRUE,
                constants.MESSAGE: constants.SUCCESS
            }
        }
        return api_return(data=data)

    # commit edited connect
    def put(self):
        coll_policy_id = views_helper.get_request_value(self.request, "coll_policy_id", "BODY")
        name = views_helper.get_request_value(self.request, "coll_policy_name", "BODY")
        command = views_helper.get_request_value(self.request, "command", "BODY")
        desc = views_helper.get_request_value(self.request, "desc", "BODY")
        ostype = views_helper.get_request_value(self.request, "ostype", "BODY")
        coll_policy_update_data = {
            'name': name,
            'cli_command': command,
            'desc': desc,
            'ostype': ostype
        }
        obj = CollPolicy.objects.get(coll_policy_id=coll_policy_id)
        serializer = CollPolicyEditSerializer(instance=obj, data=coll_policy_update_data)
        try:
            if serializer.is_valid():
                serializer.save()
                data = {
                    'data': serializer.data,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }

                }
                return api_return(data=data)
        except Exception as e:
            print e
            return exception_handler(e)

