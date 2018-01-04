#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''

@author: kimli
@contact: kimli@cisco.com
@file: policy_tree.py
@time: 2017/12/20 9:41
@desc:

'''
import os,sys
script_dir = os.path.split(os.path.realpath(__file__))[0]
prj_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.append(prj_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pantheon.Venus.db_units.settings")
import django
django.setup()
import json
from collections import OrderedDict
from backend.apolo.tools import constants
from Pantheon.Venus.db_units.models import CollPolicyRuleTree, CollPolicy, CollPolicyCliRule


class Policy_tree_node(object):

    def __init__(self):
        self.tree_id =''
        self.parent_tree_id = ''
        self.is_leaf = False
        self.level = 0
        self.rule_id_path = ''
        self.coll_policy_id =''
        self.rule_id =''
        self.rule_name = ''
        self.rule_type = None

    # test code
    def to_string(self):
        return 'tree id:{},' \
               'parent_tree_id:{},' \
               'is_leaf:{},' \
               'level:{},' \
               'rule_id_path:{},' \
               'coll_policy_id:{},' \
               'rule_id:{}'.format(self.tree_id, self.parent_tree_id, self.is_leaf,
                                   self.level, self.rule_id_path, self.coll_policy_id,
                                   self.rule_id)
class Rule_Tree(object):

    def __init__(self):
        self.block_rule_type_one = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_ONE_NAME,
            'rule_id': 0,'children': []
        }
        self.block_rule_type_two = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_TWO_NAME,
            'rule_id': 0,
            'children': []
        }
        self.block_rule_type_three ={
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_THREE_NAME,
            'rule_id': 0,
            'children': []
        }
        self.data_rule_type_one = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_ONE_NAME,
            'rule_id': 0,
            'children': []
        }
        self.data_rule_type_two = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_TWO_NAME,
            'rule_id': 0,
            'children': []
        }
        self.data_rule_type_three = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_THREE_NAME,
            'rule_id': 0,
            'children': []
        }

    def toJosn(self):
        block_rule_list=[self.block_rule_type_one, self.block_rule_type_two, self.block_rule_type_three]
        data_rule_list = [self.data_rule_type_one, self.data_rule_type_two, self.data_rule_type_three]
        return block_rule_list,data_rule_list

class Policy_tree(object):

    def __init__(self, coll_policy_id):
        # the type is dict
        self.all_nodes = OrderedDict()
        self.coll_policy_id = coll_policy_id

    # creat policy tree
    # input :all rule node list in the policy tree
    # output :json data of tree
    def get_policy_tree(self):

        policy_name = CollPolicy.objects.get(coll_policy_id=self.coll_policy_id).name
        root = {'id': 'j1',
                'text': policy_name,
                'icon': constants.POLICY_TREE_ROOT_ICON,
                'rule_id': 0,
                'children': []
                }
        node_list = self.__get_node_list__()
        return self.__get_nodes__(node_list, 0, root)

    # get all the nodes in the coll_policy_tree
    def __get_node_list__(self):

        policy_tree_query_set = CollPolicyRuleTree.objects.filter(coll_policy=self.coll_policy_id)
        node_array = []
        for item in policy_tree_query_set:
            rule = item.rule
            policy_tree_node = Policy_tree_node()
            policy_tree_node.rule_id = rule.ruleid
            policy_tree_node.rule_name = rule.name
            policy_tree_node.rule_type = rule.rule_type
            policy_tree_node.coll_policy_id = self.coll_policy_id
            policy_tree_node.tree_id = item.treeid
            if not item.parent_tree_id:
                policy_tree_node.parent_tree_id = 0
            else:
                policy_tree_node.parent_tree_id = item.parent_tree_id
            if item.is_leaf == 1:
                policy_tree_node.is_leaf = True
            policy_tree_node.level = item.level
            node_array.append(policy_tree_node)
        return node_array

    # get all the rules of the coll_policy
    def __get_rule_list__(self):
        rules_query_set = CollPolicyCliRule.objects.filter(coll_policy=self.coll_policy_id)
        return rules_query_set

    def get_rules_tree(self):

        rule_list = self.__get_rule_list__()
        rule_tree = Rule_Tree()
        for rule in rule_list:
            print type(rule)
            r ={
                'icon': '',
                'text': rule.name,
                'rule_id': rule.ruleid,
                'children': []
            }
            if rule.rule_type ==1:
                r['icon'] = constants.DATA_NODE_ICON
                rule_tree.data_rule_type_one['children'].append(r)
            elif rule.rule_type ==2:
                r['icon'] = constants.DATA_NODE_ICON
                rule_tree.data_rule_type_two['children'].append(r)
            elif rule.rule_type == 3:
                r['icon'] = constants.DATA_NODE_ICON
                rule_tree.data_rule_type_three['children'].append(r)
            elif rule.rule_type == 5:
                r['icon'] = constants.BLOCK_NODE_ICON
                rule_tree.block_rule_type_one['children'].append(r)
            elif rule.rule_type == 6:
                r['icon'] = constants.BLOCK_NODE_ICON
                rule_tree.block_rule_type_two['children'].append(r)
            elif rule.rule_type == 7:
                r['icon'] = constants.BLOCK_NODE_ICON
                rule_tree.block_rule_type_three['children'].append(r)
            else:
                print 'Error:rule type is not defined'

        return rule_tree.toJosn()

    # build policy tree
    # input:
    # node_list : list of all rule nodes in the policy tree
    # parent_node_tree_id : parent node tree id of the next node
    # tree_dict : the contents of tree
    # output : dict data of the tree

    def __get_nodes__(self, node_list, parent_node_id, tree_dict, node_num=0):

        for node in node_list:

            if node.parent_tree_id == parent_node_id:
                node_num += 1
                d = {'id': 'j1-{}'.format(node_num),
                     'text': node.rule_name,
                     'icon': '',
                     'rule_id': node.rule_id,
                     'children': []
                     }
                if node.is_leaf and node.rule_type < 5:
                    d['icon'] = constants.DATA_NODE_ICON
                else:
                    d['icon'] = constants.BLOCK_NODE_ICON
                    self.__get_nodes__(node_list, node.tree_id, d, node_num)
                tree_dict['children'].append(d)

        return tree_dict

    # get all information of nodes of tree
    # input:
    # tree_dict: dict data of the tree
    # deep : tree deep
    # parent_tree_id : parent tree id of the node
    # rules : the node's rule path from root to the node
    # output: self.all_nodes:
    # save the policy tree node instance in all_nodes.
    # save very node information in very policy tree node instance

    def get_all_nodes(self, tree_dict, deep=0, parent_tree_id=None, rules=None):
        # no leaf node
        if tree_dict.has_key('children') and tree_dict['children']:

            ptn = Policy_tree_node()
            ptn.tree_id = tree_dict['id']
            ptn.rule_id = tree_dict['rule_id']
            if rules:
                ptn.rule_id_path = rules
                rules = '{}_{}'.format(rules, tree_dict['rule_id'])
            else:
                rules = str(tree_dict['rule_id'])
            ptn.is_leaf = False
            ptn.level = deep
            ptn.parent_tree_id = parent_tree_id
            ptn.coll_policy_id =self.coll_policy_id
            # if tree_dict['rule_id']:
            self.all_nodes.update({ptn.tree_id: ptn})
            deep +=1
            for item in tree_dict['children']:
                self.get_all_nodes(item, deep, parent_tree_id=ptn.tree_id, rules=rules)
        else:
            # leaf node
            ptn = Policy_tree_node()
            ptn.tree_id = tree_dict['id']
            ptn.rule_id = tree_dict['rule_id']
            ptn.is_leaf = True
            ptn.level = deep
            ptn.coll_policy_id = self.coll_policy_id
            ptn.parent_tree_id = parent_tree_id
            ptn.rule_id_path = rules
            self.all_nodes.update({ptn.tree_id: ptn})
            return True

    # find the node Whether exist in the tree
    # input:  the tree json,policy_tree_id, rule_id
    # output : if the node exist in tree ,return True.
    #          else return False
    # note : do not connect db,but need to traverse all the tree
    def find_node(self, tree_dict, rule_id):

        if tree_dict.has_key('rule_id'):
            if tree_dict['rule_id'] == rule_id:
                return True
        if tree_dict.has_key('children'):
            for my_item in tree_dict['children']:
                if self.find_node(my_item, rule_id):
                    return True


# test code
if __name__=='__main__':
    test_tree = """{
                       "id": "j1-2",
                       "text": "b1",
                       "icon": "icon1",
                       "rule_id":"",
                       "children": [
                           {
                               "id": "j3-2",
                               "text": "b2",
                               "icon": "icon2",
                               "rule_id": 2,
                               "children": [
                                   {
                                       "id": "j3-3",
                                       "text": "d1",
                                       "icon": "icon3",
                                       "rule_id":4,
                                       "children": []
                                   },
                                   {
                                       "id": "j3-4",
                                       "text": "d2",
                                       "icon": "icon4",
                                       "rule_id": 1000054,
                                       "children": []
                                   },
                                   {
                                       "id": "j3-5",
                                       "text": "d3",
                                       "icon": "icon5",
                                       "rule_id": 1000055,
                                       "children": []
                                   }
                               ]
                           }
                       ]
                   }"""
    nodes = []
    # test_arry =[[17, 0, 0, 1, 1, 'testb1', 5], [18, 17, 1, 2, 2, 'testb2', 6], [19, 17, 1, 2, 3, 'testb2', 7], [20, 17, 1, 2, 2, 'testd1', 7]]
    # for item in test_arry:
    #     pn = Policy_tree_node()
    #     pn.tree_id = item[0]
    #     pn.parent_tree_id = item[1]
    #     if item[2] ==1:
    #         pn.is_leaf = True
    #     pn.level = item[3]
    #     pn.rule_id = item[4]
    #     pn.rule_name = item[5]
    #     pn.rule_type = item[6]
    #     nodes.append(pn)
    dict = json.loads(test_tree)
    ptn = Policy_tree(1)
    k = ptn.find_node(dict, 2)
    if k :
        print k
    else:
        print False
    # print ptn.create_policy_tree('test', nodes)

    # tp = ptn.create_rule_tree(nodes)
    # print tp[0]
    # print tp[1]