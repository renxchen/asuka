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

from backend.apolo.models import CollPolicyCliRule, CollPolicy, CollPolicyRuleTree
from backend.apolo.serializer.policytree_serializer import CollPolicyCliRuleSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree

from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class PolicyTreeRuleViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(PolicyTreeRuleViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    # get information of rules from db
    # http://127.0.0.1:8000/v1/api_policy_tree_rule/?rule_id=1&coll_pollicy_id=1

    def get(self):

        try:
            coll_policy_id = views_helper.get_request_value(self.request, key='coll_policy_id', method_type='GET')
            rule_id = views_helper.get_request_value(self.request, key='rule_id', method_type='GET')
            query_set = CollPolicyRuleTree.objects.filter(rule=rule_id, coll_policy=coll_policy_id)
            is_used = False
            if len(query_set) > 0:
                is_used = True
            rule_info = CollPolicyCliRule.objects.get(ruleid=rule_id)
            result_dict = CollPolicyCliRuleSerializer(rule_info).data
            split_char = result_dict['split_char']
            if split_char:
                if split_char == '@space@':
                    result_dict['split_char'] = 4
                    result_dict['other_char'] =None
                elif split_char == ',':
                    result_dict['split_char'] = 1
                    result_dict['other_char'] = None

                elif split_char == '/':
                    result_dict['split_char'] = 2
                    result_dict['other_char'] = None
                else:
                    result_dict['split_char'] = 3
                    result_dict['other_char'] = split_char

            data = {
                'rule_is_used': is_used,
                'data': result_dict,
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
            insert_info = views_helper.get_request_value(self.request, key='rule_info', method_type='BODY')
            coll_policy_id = str(insert_info['coll_policy'])
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
                cli_command = CollPolicy.objects.get(coll_policy_id=coll_policy_id).cli_command
                rule_data_dict = self.__set_input_rule_data__(insert_info)
                rule_data_dict['command'] = cli_command
                serializer = CollPolicyCliRuleSerializer(data=rule_data_dict)
                if serializer.is_valid():
                    serializer.save()
                    policy_tree = Policy_tree(coll_policy_id)
                    rule_tree_tuple = policy_tree.get_rules_tree()
                    data = {
                        'data': {
                            "block_rule_tree_json": rule_tree_tuple[0],
                            "data_rule_tree_json": rule_tree_tuple[1]
                        },
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

            # http://127.0.0.1:8000/v1/api_policy_tree_rule/?rule_id=1
            # check before delete rule
            rule_id = views_helper.get_request_value(self.request, 'rule_id', 'GET')
            insert_info = views_helper.get_request_value(self.request, 'rule_info', 'BODY')
            # policy_tree_id = views_helper.get_request_value(self.request, key='policy_tree_id', method_type='BODY')
            policy_tree_id = insert_info['coll_policy']
            name = insert_info['name']
            query_set_len = 0
            # judge what is the name chanced in the rule_info
            if name != CollPolicyCliRule.objects.get(ruleid=rule_id).name:
                query_set = CollPolicyCliRule.objects.filter(name=name, coll_policy=policy_tree_id)
                query_set_len = len(query_set)
            if query_set_len > 0:
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
                rule_data_dict = self.__set_input_rule_data__(insert_info)
                serializer = CollPolicyCliRuleSerializer(instance=old_rule_obj, data=rule_data_dict)
                if serializer.is_valid(Exception):
                    serializer.save()
                    new_name= serializer.data['name']
                    policy_tree = Policy_tree(policy_tree_id)
                    rule_tree_tuple = policy_tree.get_rules_tree()
                    data = {
                        'data': {
                            "new_name": new_name,
                            "block_rule_tree_json": rule_tree_tuple[0],
                            "data_rule_tree_json": rule_tree_tuple[1]
                        },
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
        # http://127.0.0.1:8000/v1/api_policy_tree_rule/?rule_id=xxx&coll_policy_id=xxx
        try:
            rule_id = views_helper.get_request_value(self.request, key='rule_id', method_type='GET')
            policy_tree_id = views_helper.get_request_value(self.request, key='coll_policy_id', method_type='GET')
            CollPolicyCliRule.objects.get(ruleid=rule_id).delete()
            p = Policy_tree(policy_tree_id)
            rule_tree_tuple = p.get_rules_tree()
            data = {
                'data': {
                    "block_rule_tree_json": rule_tree_tuple[0],
                    "data_rule_tree_json": rule_tree_tuple[1]
                },
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }

            }
            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def __set_input_rule_data__(front_data):
        rule_data_dict = {'name': front_data['name']}
        if front_data.has_key('key_str'):
            rule_data_dict['key_str'] = front_data['key_str']
        else:
            rule_data_dict['key_str'] = None

        if front_data.has_key('mark_string'):
            rule_data_dict['mark_string'] = front_data['mark_string']
        else:
            rule_data_dict['mark_string'] = None

        if front_data.has_key('split_char'):

            if int(front_data['split_char']) == 4:
                rule_data_dict['split_char'] = '@space@'
            elif int(front_data['split_char']) == 1:
                rule_data_dict['split_char'] = ','
            elif int(front_data['split_char']) == 2:
                rule_data_dict['split_char'] = '/'
            else:
                rule_data_dict['split_char'] = front_data['other_char']
        else:
            rule_data_dict['split_char'] = None

        if front_data.has_key('x_offset'):
            rule_data_dict['x_offset'] = front_data['x_offset']
        else:
            rule_data_dict['x_offset'] = None

        if front_data.has_key('y_offset'):
            rule_data_dict['y_offset'] = front_data['y_offset']
        else:
            rule_data_dict['y_offset'] = None

        if front_data.has_key('line_nums'):
            rule_data_dict['line_nums'] = front_data['line_nums']
        else:
            rule_data_dict['line_nums'] = None

        if front_data.has_key('rule_type'):

            arry = front_data['rule_type'].split('_')
            if arry[0] == 'block':
                rule_data_dict['rule_type'] = int(arry[2]) + 4
            else:
                rule_data_dict['rule_type'] = arry[2]
        else:
            rule_data_dict['rule_type'] = None

        if front_data.has_key('end_mark_string'):
            rule_data_dict['end_mark_string'] = front_data['end_mark_string']
        else:
            rule_data_dict['end_mark_string'] = None

        if front_data.has_key('start_line_num'):
            rule_data_dict['start_line_num'] = front_data['start_line_num']
        else:
            rule_data_dict['start_line_num'] = None

        if front_data.has_key('end_line_num'):
            rule_data_dict['end_line_num'] = front_data['end_line_num']
        else:
            rule_data_dict['end_line_num'] = None

        if front_data.has_key('is_serial'):
            rule_data_dict['is_serial'] = int(front_data['is_serial'])
        else:
            rule_data_dict['is_serial'] = None

        if front_data.has_key('is_include'):
            rule_data_dict['is_include'] = front_data['is_include']
        else:
            rule_data_dict['is_include'] = None

        if front_data.has_key('command'):
            rule_data_dict['command'] = front_data['command']
        else:
            rule_data_dict['command'] = None

        if front_data.has_key('coll_policy'):
            rule_data_dict['coll_policy'] = front_data['coll_policy']
        else:
            rule_data_dict['coll_policy'] = None

        if front_data.has_key('desc'):
            rule_data_dict['desc'] = front_data['desc']
        else:
            rule_data_dict['desc'] = None

        if front_data.has_key('extract_key'):
            rule_data_dict['extract_key'] = front_data['extract_key']
        else:
            if rule_data_dict['rule_type'] >4:
                rule_data_dict['extract_key'] = None
            else:
                rule_data_dict['extract_key'] = '.*'

        if front_data.has_key('value_type'):
            rule_data_dict['value_type'] = front_data['value_type']
        else:
            rule_data_dict['value_type'] = None

        print rule_data_dict
        return rule_data_dict
