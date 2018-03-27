#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: kimli
@contact: kimli@cisco.com
@file: policy_tree_rule_view.py
@time: 2017/12/25 17:37
@desc:
"""
import traceback

from django.db.models import Q
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree
from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.models import CollPolicyCliRule, CollPolicy, CollPolicyRuleTree, DataTable
from backend.apolo.serializer.policytree_serializer import CollPolicyCliRuleSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class PolicyTreeRuleViewSet(viewsets.ViewSet):

    def __init__(self, request, **kwargs):
        super(PolicyTreeRuleViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')

    def get(self):
        """!@brief
        load the rule information when open the rule edit page
        @param
        @pre
        @post
        @return rule information,verify result(rule_is_used,is_processing,is_locked)
        @author kimli
        @date 2017/12/25
        """
        try:
            coll_policy_id = views_helper.get_request_value(self.request, key='coll_policy_id', method_type='GET')
            rule_id = views_helper.get_request_value(self.request, key='rule_id', method_type='GET')
            query_set = CollPolicyRuleTree.objects.filter(rule=rule_id, coll_policy=coll_policy_id)
            is_used = False
            is_processing = False
            is_locked = False
            if len(query_set) > 0:
                is_processing = self.__judge_rule_is_processing(coll_policy_id)
                is_locked = self.__judge_rule_is_locked(rule_id, coll_policy_id)
                is_used = True
            rule_info = CollPolicyCliRule.objects.get(ruleid=rule_id)
            result_dict = CollPolicyCliRuleSerializer(rule_info).data
            split_char = result_dict['split_char']
            if split_char:
                if split_char == '@space@':
                    result_dict['split_char'] = 4
                    result_dict['other_char'] = None
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
                'is_processing': is_processing,
                'is_locked': is_locked,
                'data': result_dict,
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        """!@brief
        save the rule information into db.
        two points need to check before save the rule information
        1 the rule name is not existing in the cp
        2 the identifier(識別子）name is not existing in the cp
        @param
        @pre
        @post
        @note
        @return data rule tree and block rule tree and verify error message
        @author kimli
        @date 2017/12/25
        """
        try:
            insert_info = views_helper.get_request_value(self.request, key='rule_info', method_type='BODY')
            coll_policy_id = str(insert_info['coll_policy'])
            name = insert_info['name']
            query_set = CollPolicyCliRule.objects.filter(name=name, coll_policy=coll_policy_id)
            error_msg_list = {}
            if len(query_set) > 0:
                error_msg_list.update({'rule_name': False})
            else:
                error_msg_list.update({'rule_name': True})

            identifier_is_existing = self.__judge_identifier_name_exist(insert_info['key_str'], coll_policy_id)
            if identifier_is_existing:
                error_msg_list.update({'key_str_name': False})
            else:
                error_msg_list.update({'key_str_name': True})

            if len(query_set) > 0 or identifier_is_existing:
                data = {
                    'data': '',
                    'verify_error_msg': error_msg_list,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.RULE_NAME_IS_EXISTENCE
                    }
                }

            else:
                cli_command = CollPolicy.objects.get(coll_policy_id=coll_policy_id).cli_command
                rule_data_dict = self.__set_input_rule_data(insert_info)
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
                        'verify_error_msg': None,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                else:
                    data = {
                        'data': serializer.errors,
                        'verify_error_msg': None,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.RULE_DATA_VALID_ERROR
                        }
                    }

            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        """!@brief
        update the rule information.
        two points need to check before update the rule information
         1 the rule name is not existing in the cp
         2 the identifier(識別子）name is not existing in the cp
        @param
        @pre
        @post
        @note
        @return data rule tree and block rule tree and verify error message
        @author kimli
        @date 2017/12/25
        """
        try:
            rule_id = int(views_helper.get_request_value(self.request, 'rule_id', 'GET'))
            insert_info = views_helper.get_request_value(self.request, 'rule_info', 'BODY')
            policy_id = insert_info['coll_policy']
            name = insert_info['name']
            query_set_len = len(CollPolicyCliRule.objects.filter(Q(name=name) &
                                                                 Q(coll_policy=policy_id) &
                                                                 ~Q(ruleid=rule_id)))

            error_msg_list = {}
            if query_set_len > 0:
                error_msg_list.update({'rule_name': False})
            else:
                error_msg_list.update({'rule_name': True})
            identifier_is_existing = self.__judge_identifier_name_exist(insert_info['key_str'], policy_id,
                                                                        rule_id=rule_id)
            if identifier_is_existing:
                error_msg_list.update({'key_str_name': False})
            else:
                error_msg_list.update({'key_str_name': True})

            if query_set_len > 0 or identifier_is_existing:
                data = {
                    'data': '',
                    'new_token': self.new_token,
                    'verify_error_msg': error_msg_list,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.FAILED
                    }
                }
            else:
                old_rule_obj = CollPolicyCliRule.objects.get(ruleid=rule_id)
                rule_data_dict = self.__set_input_rule_data(insert_info)
                serializer = CollPolicyCliRuleSerializer(instance=old_rule_obj, data=rule_data_dict)
                if serializer.is_valid(Exception):
                    serializer.save()
                    new_name = serializer.data['name']
                    policy_tree = Policy_tree(policy_id)
                    rule_tree_tuple = policy_tree.get_rules_tree()
                    data = {
                        'data': {
                            "new_name": new_name,
                            "block_rule_tree_json": rule_tree_tuple[0],
                            "data_rule_tree_json": rule_tree_tuple[1]
                        },
                        'verify_error_msg': None,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }

                    }
                else:
                    data = {
                        'data': '',
                        'new_token': self.new_token,
                        'verify_error_msg': None,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.RULE_DATA_VALID_ERROR
                        }
                    }

            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        """!@brief
       delete the rule
       @param
       @pre
       @post
       @note
       @return data rule tree and block rule tree
       @author kimli
       @date 2017/12/25
       """
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
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)


    def __set_input_rule_data(self, front_data):
        """!@brief
        sort out data from the front web page
        @param front_data: the data from the front web page
        @pre
        @post
        @note
        @return the sorted out rule information
        @author kimli
        @date 2017/12/25
        """
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
            rule_data_dict['extract_key'] = None

        rule_data_dict['value_type'] = self.__get_value_type(rule_data_dict['rule_type'],
                                                             rule_data_dict['extract_key'])

        return rule_data_dict

    @staticmethod
    def __get_value_type(rule_type, extract_data_reg):
        """!@brief
        judge regular expression extract what is value type of data
        @param rule_type:rule type ,extract_data_reg:regular expression
        @pre
        @post
        @note
        @return the sorted out rule information
        @author kimli
        @date 2017/12/25
        """
        int_reg = ['\d+', '\d', '\d+$', '\d$', '-\d+', '-\d', '-\d+$', '-\d$']
        float_reg = ['\d\.\d', '\d\.\d+', '\d+\.\d', '\d+\.\d+', '\d\.\d$', '\d\.\d+$', '\d+\.\d$', '\d+\.\d+$',
                     '-\d\.\d', '-\d\.\d+', '-\d+\.\d', '-\d+\.\d+', '-\d\.\d$', '-\d\.\d+$', '-\d+\.\d$', '-\d+\.\d+$'
                     ]
        if rule_type == '4':
            return constants.VALUE_TYPE_INT
        elif rule_type == '9':
            return constants.VALUE_TYPE_TEXT
        else:
            if extract_data_reg in int_reg:
                return constants.VALUE_TYPE_INT
            elif extract_data_reg in float_reg:
                return constants.VALUE_TYPE_FLOAT
            else:
                return constants.VALUE_TYPE_STRING

    @staticmethod
    def __judge_identifier_name_exist(identifier_name, policy_id, rule_id=0):
        """!@brief
        judge identifier name(識別子名) is not  existing in the cp
        @param identifier_name:識別子名 ,policy id:policy id
        @pre
        @post
        @note
        @return the sorted out rule information
        @author kimli
        @date 2017/12/25
        """
        query_result = CollPolicyCliRule.objects.filter(Q(key_str=identifier_name) &
                                                        Q(coll_policy=policy_id) &
                                                        ~Q(ruleid=rule_id))
        if len(query_result) > 0:
            return True
        else:
            return False

    @staticmethod
    def __judge_rule_is_processing(coll_policy_id):
        """!@brief
        judge the cp that include the rule, whether is running or not
        @param coll_policy_id: collection policy id
        @pre
        @post call the function : Tool.get_policy_status(policy_id)
        @note
        @return if the policy is running, return True. if the policy is not running, return False
        @author kimli
        @date 2017/12/25
        """
        return Tool.get_policy_status(coll_policy_id)

    @staticmethod
    def __judge_rule_is_locked(rule_id, coll_policy_id):
        """!@brief
       judge the rule status is lock
       if  the tree_id corresponding to the rule_id is existing in the data_table table,
       the rule status is lock,else is not lock
       @param rule_id:rule id, coll_policy_id:collection policy id
       @pre
       @post
       @note
       @return if the rule status is lock ,return True.if the status is not lock,return False
       @author kimli
       @date 2017/12/25
       """
        tree_id = CollPolicyRuleTree.objects.filter(rule=rule_id, coll_policy=coll_policy_id).values('treeid')
        tree_count = len(DataTable.objects.filter(tree__in=tree_id))
        if tree_count > 0:
            return True
        else:
            return False
