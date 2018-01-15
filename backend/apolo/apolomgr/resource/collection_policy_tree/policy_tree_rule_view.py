#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: policy_tree_rule_view.py
@time: 2017/12/25 17:37
@desc:

'''
import traceback

from rest_framework import viewsets

from backend.apolo.models import CollPolicyCliRule
from backend.apolo.serializer.policytree_serializer import CollPolicyCliRuleSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree
import json

from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class PolicyTreeRuleViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(PolicyTreeRuleViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    # get information of rules from db
    # http://127.0.0.1:8000/v1/api_policy_tree_rule/?rule_id=1
    def get(self):
        try:
            rule_id = views_helper.get_request_value(self.request, key='rule_id', method_type='GET')
            rule_info = CollPolicyCliRule.objects.get(ruleid=rule_id)
            serializer = CollPolicyCliRuleSerializer(rule_info)
            data = {
                'data': '',
                'rule_info': serializer.data,
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


    # save the rule into db
    # 1 check the rule name is existing in the rules of the tree when updating the rule
    # 2 if the name is exists,return error.else to step 3
    # 3 save the rule into db
    # 4 get all rules of tree ,and return the information to front
    def post(self):
        try:
            data = {}
            insert_info = views_helper.get_request_value(self.request, key='rule_info', method_type='BODY')
            coll_policy_id = insert_info['coll_policy']
            name = insert_info['name']
            query_set = CollPolicyCliRule.objects.filter(name=name, coll_policy=coll_policy_id)
            if len(query_set) > 0:
                data = {
                    'data': '',
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.RULE_NAME_IS_EXISTENCE
                    }
                }
            else:
                serializer = CollPolicyCliRuleSerializer(data=insert_info)
                if serializer.is_valid():
                    serializer.save()
                    policy_tree = Policy_tree(coll_policy_id)
                    rule_tree_tuple = policy_tree.get_rules_tree()
                    data = {
                        'data': '',
                        "block_rule_tree_json": rule_tree_tuple[0],
                        "data_rule_tree_json": rule_tree_tuple[1],
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                else:
                    data = {
                        'data': serializer.errors,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.RULE_DATA_VALID_ERROR
                        }
                    }

            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    # 1 check the rule name is existing in the rules of the tree when updating the rule
    # 2 if the name is different,do update,else raise error
    # 3 get all rules of tree ,and return the information to front
    def put(self):
        try:
            insert_info = views_helper.get_request_value(self.request, 'rule_info', 'BODY')
            # policy_tree_id = views_helper.get_request_value(self.request, key='policy_tree_id', method_type='BODY')
            policy_tree_id = insert_info['coll_policy']
            name = insert_info['name']
            rule_id = insert_info['rule_id']
            query_set = []
            data = {}
            # judge what is the name chanced in the rule_info
            if name != CollPolicyCliRule.objects.get(ruleid=rule_id).name:
                query_set = CollPolicyCliRule.objects.filter(name=name, coll_policy=policy_tree_id)
            if len(query_set) > 0:
                data = {
                    'data': '',
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.RULE_NAME_IS_EXISTENCE
                    }
                }
            else:
                old_rule_obj = CollPolicyCliRule.objects.get(ruleid=rule_id)
                serializer = CollPolicyCliRuleSerializer(instance=old_rule_obj, data=insert_info)
                if serializer.is_valid():
                    serializer.save()
                    policy_tree = Policy_tree(policy_tree_id)
                    rule_tree_tuple = policy_tree.get_rules_tree()
                    data = {
                        'data': '',
                        "block_rule_tree_json": rule_tree_tuple[0],
                        "data_rule_tree_json": rule_tree_tuple[1],
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }

                    }
                else:
                    data = {
                        'data': '',
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.RULE_DATA_VALID_ERROR
                        }
                    }

            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        # http://127.0.0.1:8000/v1/api_policy_tree_rule/?rule_id=xxx&policy_tree_id=xxx
        try:
            rule_id = views_helper.get_request_value(self.request, key='rule_id', method_type='GET')
            policy_tree_id = views_helper.get_request_value(self.request, key='policy_tree_id', method_type='GET')
            CollPolicyCliRule.objects.get(ruleid=rule_id).delete()
            p = Policy_tree(policy_tree_id)
            rule_tree_tuple = p.get_rules_tree()
            data = {
                'data': '',
                "block_rule_tree_json": rule_tree_tuple[0],
                "data_rule_tree_json": rule_tree_tuple[1],
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }

            }
            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)
