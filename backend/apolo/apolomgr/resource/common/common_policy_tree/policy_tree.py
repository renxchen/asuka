#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: policy_tree.py
@time: 2017/12/20 9:41
@desc:
"""
from collections import OrderedDict

from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.db_utils.db_opt import DBOpt
from backend.apolo.tools import constants


class Policy_tree_node(object):
    def __init__(self):
        self.tree_id = ''
        self.parent_tree_id = ''
        self.is_leaf = False
        self.level = 0
        self.rule_id_path = ''
        self.coll_policy_id = ''
        self.rule_id = ''
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
        """!@brief
        init parent node of rules
        @param
        @pre
        @post
        @note
        @return
        @author Gin Chen
        @date 2017/12/20
        """
        self.block_rule_type_one = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_ONE_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'block_rule_1'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }

        self.block_rule_type_two = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_TWO_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'block_rule_2'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.block_rule_type_three = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_THREE_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'block_rule_3'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.block_rule_type_four = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.BLOCK_RULE_TREE_KIND_FOUR_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'block_rule_4'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.data_rule_type_one = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_ONE_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'data_rule_1'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.data_rule_type_two = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_TWO_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'data_rule_2'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.data_rule_type_three = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_THREE_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'data_rule_3'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.data_rule_type_four = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_FOUR_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'data_rule_4'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        self.data_rule_type_five = {
            'icon': constants.RULE_NODE_ICON,
            'text': constants.DATA_RULE_TREE_KIND_FIVE_NAME,
            'data': {
                'rule_id': 0,
                'is_root': True,
                'rule_type': 'data_rule_9'
            },
            'state': {
                'opened': True,
            },
            'children': []
        }

    def toReturn(self):
        """!@brief
        return data rule tree and block rule tree
        @param
        @pre
        @post
        @note
        @return data rule tree and block rule tree
        @author Gin Chen
        @date 2017/12/20
        """
        block_rule_list = [self.block_rule_type_one, self.block_rule_type_two, self.block_rule_type_three,
                           self.block_rule_type_four]
        data_rule_list = [self.data_rule_type_one, self.data_rule_type_two,
                          self.data_rule_type_three, self.data_rule_type_four, self.data_rule_type_five]
        return block_rule_list, data_rule_list


class Policy_tree(DBOpt):
    def __init__(self, coll_policy_id):
        # the type is dict
        self.all_nodes = OrderedDict()
        self.coll_policy_id = coll_policy_id


    def get_policy_tree(self):
        """!@brief
        create collection policy tree
        @param
        @pre
        @post
        @note input:all rule node list in the policy tree
        @return json data of tree
        @author Gin Chen
        @date 2017/12/20
        """
        root = {
            'text': constants.COLLECTION_POLICY_TREE_NAME,
            'icon': constants.POLICY_TREE_ROOT_ICON,
            'data': {
                'rule_type': '',
                'rule_id': 0,
                'tree_id': 0,
                'is_root': True,
            },
            'state': {
                'opened': True,
            },
            'children': []
        }
        node_list = self.__get_node_list()
        return self.__get_nodes(node_list, 0, root)


    def __get_node_list(self):
        """!@brief
        get all the nodes in the coll_policy_tree
        @param
        @pre
        @post
        @note
        @return all nodes of the tree
        @author Gin Chen
        @date 2017/12/20
        """
        policy_tree_query_set = self.get_tree_detail_from_db(self.coll_policy_id)
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

    def get_rules_tree(self):
        """!@brief
        create rule trees
        @param
        @pre
        @post
        @note
        @return data rule tree and block rule tree
        @author Gin Chen
        @date 2017/12/20
        """
        rule_list = self.get_many_rules_detail_from_db(self.coll_policy_id)
        rule_tree = Rule_Tree()
        err_having = False
        for rule in rule_list:
            r = {
                'icon': '',
                'text': rule.name,
                'data': {
                    'rule_id': rule.ruleid,
                    'rule_type': ''
                },
                'children': []
            }
            if rule.rule_type == 1:
                r['icon'] = constants.DATA_NODE_ICON
                r['data']['rule_type'] = 'data_rule_1'
                rule_tree.data_rule_type_one['children'].append(r)
            elif rule.rule_type == 2:
                r['icon'] = constants.DATA_NODE_ICON
                r['data']['rule_type'] = 'data_rule_2'
                rule_tree.data_rule_type_two['children'].append(r)
            elif rule.rule_type == 3:
                r['icon'] = constants.DATA_NODE_ICON
                r['data']['rule_type'] = 'data_rule_3'
                rule_tree.data_rule_type_three['children'].append(r)
            elif rule.rule_type == 4:
                r['icon'] = constants.DATA_NODE_ICON
                r['data']['rule_type'] = 'data_rule_4'
                rule_tree.data_rule_type_four['children'].append(r)
            elif rule.rule_type == 5:
                r['icon'] = constants.BLOCK_NODE_ICON
                r['data']['rule_type'] = 'block_rule_1'
                rule_tree.block_rule_type_one['children'].append(r)
            elif rule.rule_type == 6:
                r['icon'] = constants.BLOCK_NODE_ICON
                r['data']['rule_type'] = 'block_rule_2'
                rule_tree.block_rule_type_two['children'].append(r)
            elif rule.rule_type == 7:
                r['icon'] = constants.BLOCK_NODE_ICON
                r['data']['rule_type'] = 'block_rule_3'
                rule_tree.block_rule_type_three['children'].append(r)
            elif rule.rule_type == 8:
                r['icon'] = constants.BLOCK_NODE_ICON
                r['data']['rule_type'] = 'block_rule_4'
                rule_tree.block_rule_type_four['children'].append(r)
            elif rule.rule_type == 9:
                r['icon'] = constants.DATA_NODE_ICON
                r['data']['rule_type'] = 'data_rule_9'
                rule_tree.data_rule_type_five['children'].append(r)
            else:
                err_having = True
                break
        if err_having:
            return 'Error', constants.LOAD_RULE_TYPE_ERROR
        else:
            return rule_tree.toReturn()

    def __get_nodes(self, node_list, parent_node_id, tree_dict, node_num=0):
        """!@brief
       get all nodes and build policy tree
       @param node_list: list of all rule nodes in the policy tree
       @param parent_node_id: parent node tree id of the next node
       @param tree_dict: the contents of tree
       @param node_num: node num
       @pre
       @post
       @note
       @return dict data of tree
       @author Gin Chen
       @date 2017/12/20
       """
        for node in node_list:

            if node.parent_tree_id == parent_node_id:
                node_num += 1
                d = {
                     'text': node.rule_name,
                     'icon': '',
                     'data': {
                         'rule_type': Tool.set_rule_type(node.rule_type),
                         'rule_id': node.rule_id,
                         'tree_id': node.tree_id
                     },
                     'state': {
                        'opened': True,
                     },
                     'children': []
                     }
                if node.is_leaf and (node.rule_type < 5 or node.rule_type ==9):
                    d['icon'] = constants.DATA_NODE_ICON
                else:
                    d['icon'] = constants.BLOCK_NODE_ICON
                    self.__get_nodes(node_list, node.tree_id, d, node_num)
                tree_dict['children'].append(d)

        return tree_dict

    def get_all_nodes(self, tree_dict, deep=0, parent_tree_id=None, rules=None):
        """!@brief
        get all information of nodes of tree
        @param tree_dict:dict data of the tree
        @param deep: the deep of tree
        @param parent_tree_id : parent tree id of the node
        @param rules : the node's rule path from root to the node
        @pre
        @post
        @note
        @return all nodes
        @author Gin Chen
        @date 2017/12/20
        """
        # no leaf node
        if tree_dict.has_key('children') and tree_dict['children']:

            ptn = Policy_tree_node()
            ptn.tree_id = tree_dict['id']
            ptn.rule_id = tree_dict['data']['rule_id']
            if rules:
                ptn.rule_id_path = rules
                rules = '{}_{}'.format(rules, tree_dict['data']['rule_id'])
            else:
                rules = str(tree_dict['data']['rule_id'])
            ptn.is_leaf = False
            ptn.level = deep
            ptn.parent_tree_id = parent_tree_id
            ptn.coll_policy_id = self.coll_policy_id
            # if tree_dict['rule_id']:
            self.all_nodes.update({ptn.tree_id: ptn})
            deep += 1
            for item in tree_dict['children']:
                self.get_all_nodes(item, deep, parent_tree_id=ptn.tree_id, rules=rules)
        else:
            # leaf node
            ptn = Policy_tree_node()
            ptn.tree_id = tree_dict['id']
            ptn.rule_id = tree_dict['data']['rule_id']
            ptn.is_leaf = True
            ptn.level = deep
            ptn.coll_policy_id = self.coll_policy_id
            ptn.parent_tree_id = parent_tree_id
            ptn.rule_id_path = rules
            self.all_nodes.update({ptn.tree_id: ptn})
            return True

    def find_node(self, tree_dict, rule_id):
        """!@brief
        judge the node that is exist in the tree or not
        @param tree_dict: json data of tree
        @param rule_id: rule id of the clicked node
        @pre
        @post
        @note
        @return  if the node exist in tree ,return True.else,return False
        @author Gin Chen
        @date 2017/12/20
        """
        if tree_dict.has_key('rule_id'):
            if tree_dict['data']['rule_id'] == rule_id:
                return True
        if tree_dict.has_key('children'):
            for my_item in tree_dict['children']:
                if self.find_node(my_item, rule_id):
                    return True

