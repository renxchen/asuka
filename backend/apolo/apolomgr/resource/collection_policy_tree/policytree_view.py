#!/usr/bin/env python

"""
@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: policytree_view.py
@time: 2017/12/18 18:24
@desc:
"""
import traceback

from django.db import transaction
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree
from backend.apolo.models import CollPolicy, CollPolicyRuleTree, Items, PolicysGroups
from backend.apolo.serializer.policytree_serializer import CollPolicyRuleTreeSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class PolicyTreeViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(PolicyTreeViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.raw_data = ''
        self.tree_id = ''
        self.tree = ''
        self.coll_policy_id = ''

    def get(self):
        """!@brief
        init policy tree edit page
        @note
        @return policy tree info,data rule rule,block rule
        @author Gin Chen
        @date 2017/12/18
        """
        try:
            self.coll_policy_id = views_helper.get_request_get(self.request, 'coll_policy_id')
            cp = CollPolicy.objects.get(coll_policy_id=self.coll_policy_id)
            cli_command_result = cp.cli_command_result
            policy_name = cp.name
            policy_tree = Policy_tree(self.coll_policy_id)
            # get policy tree
            policy_tree_dict = policy_tree.get_policy_tree()
            # get rules of the policy tree
            rule_tree_tuple = policy_tree.get_rules_tree()
            if rule_tree_tuple == 'Error':
                data = {
                    'data': '',
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.LOAD_RULE_TYPE_ERROR
                    }
                }
            else:
                block_rule_tree_dict = rule_tree_tuple[0]
                data_rule_tree_dict = rule_tree_tuple[1]
                data = {
                    'data': {
                        "coll_policy_name": policy_name,
                        "cli_command_result": cli_command_result,
                        "policy_tree_json": policy_tree_dict,
                        "block_rule_tree_json": block_rule_tree_dict,
                        "data_rule_tree_json": data_rule_tree_dict,
                    },
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
        save policy tree
        @note
        @return response
        @author Gin Chen
        @date 2017/12/18
        """
        self.coll_policy_id = views_helper.get_request_value(self.request, 'coll_policy_id', 'BODY')
        self.tree = views_helper.get_request_value(self.request, 'tree', 'BODY')
        self.raw_data = views_helper.get_request_value(self.request, 'raw_data', 'BODY')
        try:

            with transaction.atomic():
                tree_is_exits = CollPolicyRuleTree.objects.filter(coll_policy=self.coll_policy_id)
                if tree_is_exits:
                    # check the policy is exits in the item tables
                    items_list = Items.objects.filter(coll_policy=self.coll_policy_id)
                    if len(items_list) > 0:
                        data = {
                            'data': '',
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.POLICY_IS_APPLIED
                            }
                        }
                        return api_return(data=data)
                    else:
                        # del the old policy tree
                        CollPolicyRuleTree.objects.filter(coll_policy=self.coll_policy_id).delete()
                # check the leaf that is not block rule
                if not self.__check_the_node_is_leaf(self.tree):
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.LEAF_IS_BLOCK_RULE
                        }
                    }
                    return api_return(data=data)

                # save the new policy
                # update cli_command_result into coll_policy table
                coll_policy = CollPolicy.objects.get(pk=self.coll_policy_id)
                if self.raw_data:
                    coll_policy.cli_command_result = self.raw_data
                    coll_policy.save()
                    # select all nodes of the policy tree
                policy_tree = Policy_tree(self.coll_policy_id)
                policy_tree.get_all_nodes(self.tree)
                obj = policy_tree.all_nodes
                data = self.__save_the_policy_tree(nodes_dict=obj)
                return api_return(data=data)

        except Exception as e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            data = {
                'data': '',
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.DB_EXCEPTION
                }
            }
            return api_return(data=data)

    def __save_the_policy_tree(self, nodes_dict):
        """!@brief
        save policy tree
        @note
        @return policy tree
        @author Gin Chen
        @date 2017/12/18
        """
        add_result = {}
        # insert  the tree node information into db
        for k, v in nodes_dict.items():
            # not root node
            if v.rule_id:
                if v.is_leaf:
                    isLeaf = 1
                else:
                    isLeaf = 0
                tree_data = {
                    'parent_tree_id': None,
                    'is_leaf': isLeaf,
                    'level': v.level,
                    'rule_id_path': v.rule_id_path,
                    'coll_policy': self.coll_policy_id,
                    'rule': v.rule_id
                }
                if add_result[v.parent_tree_id] is not 'root':
                    tree_data['parent_tree_id'] = add_result[v.parent_tree_id]

                serializer = CollPolicyRuleTreeSerializer(data=tree_data)
                if serializer.is_valid():
                    serializer.save()
                    tree_id = serializer.data['treeid']
                    add_result.update({k: tree_id})
                else:
                    data = {
                        'data': serializer.errors,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.POLICY_DATA_VALID_ERROR
                        }
                    }
                    return data
            else:
                # root node
                add_result.update({k: 'root'})
        data = {
            'data': '',
            'coll_policy_id': self.coll_policy_id,
            'new_token': self.new_token,
            constants.STATUS: {
                constants.STATUS: constants.TRUE,
                constants.MESSAGE: constants.SUCCESS
            }
        }
        return data

    def __check_the_node_is_leaf(self, tree_dict):
        """!@brief
       check the leaf node is data rule or not
       @note
       @return if the leaf node is data rule ,return True ,else return False
       @author Gin Chen
       @date 2017/12/18
       """
        rule_type = tree_dict['data']['rule_type'].split('_')[0]
        if tree_dict.has_key('children'):
            if len(tree_dict['children']) > 0:
                block_is_leaf = False
                for children in tree_dict['children']:
                    block_is_leaf = self.__check_the_node_is_leaf(children)
                    if not block_is_leaf:
                        break
                return block_is_leaf
            else:
                if rule_type == 'block':
                    return False
                else:
                    return True

    def __check_policy_tree_in_group(self):
        """!@brief
       check the policy that is in policy group or not
       @note
       @return if the policy in policy group,return False.else,return True
       @author Gin Chen
       @date 2017/12/18
       """
        queryset = PolicysGroups.objects.filter(policy=self.coll_policy_id)
        if queryset.count() > 0:
            return False
        else:
            return True
