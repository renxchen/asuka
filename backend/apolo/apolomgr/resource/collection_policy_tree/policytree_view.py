#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: policytree_view.py
@time: 2017/12/18 18:24
@desc:

'''
import json

from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree, Policy_tree_node
from backend.apolo.models import CollPolicy, CollPolicyRuleTree, CollPolicyCliRule
from backend.apolo.serializer.policytree_serializer import CollPolicyRuleTreeSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.views_helper import api_return


class PolicyTreeViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(PolicyTreeViewSet, self).__init__(**kwargs)
        #self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.request = request
        self.raw_data = ''
        self.tree_id = ''
        self.tree= ''
        self.coll_policy_id = ''

    # init policy tree edit page
    # input coll_policy_id
    # init context include:
    # 1 get cli_command_result from coll_policy table
    # 2 get policy tree
    # 3 get policy tree rules
    # notice : get 2 and 3 step 's data by table(coll_policy_rule_tree and coll_policy_cli_rule) connection
    def get(self):
        # v1/api_policy_tree/?coll_policy_id=xxx
        self.coll_policy_id = views_helper.get_request_get(self.request, 'coll_policy_id')
        cp = CollPolicy.objects.get(coll_policy_id=self.coll_policy_id)
        cli_command_result = cp.cli_command_result
        policy_name = cp.name
        policy_tree = Policy_tree(self.coll_policy_id)
        # get policy tree
        policy_tree_dict = policy_tree.get_policy_tree()
        # get rules of the policy tree
        rule_tree_tuple = policy_tree.get_rules_tree()
        block_rule_tree_dict = rule_tree_tuple[0]
        data_rule_tree_dict = rule_tree_tuple[1]
        data ={
            "coll_policy_name": policy_name,
            "cli_command_result": cli_command_result,
            "policy_tree_json": policy_tree_dict,
            "block_rule_tree_json": block_rule_tree_dict,
            "data_rule_tree_json": data_rule_tree_dict,
            constants.STATUS: constants.TRUE,
            constants.MESSAGE: constants.SUCCESS
        }

        return api_return(data=data)



    # save policy tree/update policy tree(update coding)
    # which things are saved into db
    # 1 update cli_command_result into coll_policy table
    # 2 if the tree is a new tree ,save tree into coll_policy_rule_tree
    # 3 else update the tree
    # notice: rule(data ,block) name must diff in the same policy tree(check in front?)
    # input: tree and coll_policy_id and raw_data
    # output : message and data that include tree and updated coll_policy context
    def post(self):
        self.tree = """{
                                   "id": "j1-2",
                                   "text": "b1",
                                   "icon": "icon1",
                                   "rule_id":0,
                                   "children": [
                                       {
                                           "id": "j3-2",
                                           "text": "b2",
                                           "icon": "icon2",
                                           "rule_id": 1,
                                           "children": [
                                               {
                                                   "id": "j3-3",
                                                   "text": "d1",
                                                   "icon": "icon3",
                                                   "rule_id":2,
                                                   "children": []
                                               },
                                               {
                                                   "id": "j3-4",
                                                   "text": "d2",
                                                   "icon": "icon4",
                                                   "rule_id": 4,
                                                   "children": []
                                               },
                                               {
                                                   "id": "j3-5",
                                                   "text": "d3",
                                                   "icon": "icon5",
                                                   "rule_id": 4,
                                                   "children": []
                                               }
                                           ]
                                       }
                                   ]
                               }"""
        self.coll_policy_id = 1
        self.raw_data = 'test raw data'
        #self.coll_policy_id =views_helper.get_request_body(self.request, 'coll_policy_id')
        #self.tree = views_helper.get_request_body(self.request, 'tree')

        # update cli_command_result into coll_policy table
        coll_policy = CollPolicy.objects.get(pk=self.coll_policy_id)
        if self.raw_data:
            coll_policy.cli_command_result=self.raw_data
            coll_policy.save()
        return_data = {
            'tree': self.tree,
                     'coll_policy_id': coll_policy.coll_policy_id,
                     'name': coll_policy.name,
                     'cli_command': coll_policy.cli_command,
                     'desc': coll_policy.desc,
                     constants.STATUS: constants.TRUE,
                     constants.MESSAGE: constants.SUCCESS
        }
        # judge  whether the coll_policy_id is in coll_policy_rule_tree
        query_result = CollPolicyRuleTree.objects.filter(coll_policy=self.coll_policy_id)
        if query_result.count() ==0:
            # the tree is a new tree
            # insert policy tree into coll_policy_rule_tree
            policy_tree = Policy_tree(self.coll_policy_id)
            policy_tree.get_all_nodes(json.loads(self.tree))
            obj = policy_tree.all_nodes
            add_result={}
            for k, v in obj.items():
                # not root node
                if v.rule_id:
                    if v.is_leaf:
                        isLeaf = 1
                    else:
                        isLeaf = 0
                    data={
                        'parent_tree_id': None,
                        'is_leaf': isLeaf,
                        'level': v.level,
                        'rule_id_path': v.rule_id_path,
                        'coll_policy': self.coll_policy_id,
                        'rule': v.rule_id
                    }
                    if add_result[v.parent_tree_id] is not 'root':
                        data['parent_tree_id'] = add_result[v.parent_tree_id]

                    serializer = CollPolicyRuleTreeSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        tree_id =serializer.data['treeid']
                        add_result.update({k: tree_id})
                    else:
                        data = {
                            'data': serializer.errors,
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.FAILED
                        }
                        return api_return(data=data)
                else:
                    # root node
                    add_result.update({k: 'root'})
        else:
            # the tree is exists in db. it need to update

            pass
        return api_return(data=return_data)

    # edit policy tree
    def put(self):
        pass

    # delete policy tree
    def delete(self):
        pass
