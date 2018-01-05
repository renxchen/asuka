#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: db_opt.py
@time: 2018/1/4 11:30
@desc:

'''
from db_until import *
from backend.apolo.models import CollPolicyCliRule, CollPolicy, CollPolicyRuleTree


class DBOpt(object):


    @staticmethod
    def get_rule_detail_from_db(rule_id):
        obj = CollPolicyCliRule.objects.get(ruleid=rule_id)
        return obj

    @staticmethod
    def get_many_rules_detail_from_db(policy_tree_id):
        rules_query_set = CollPolicyCliRule.objects.filter(coll_policy=policy_tree_id)
        return rules_query_set

    @staticmethod
    def get_tree_detail_from_db(policy_tree_id):
        query_set = CollPolicyRuleTree.objects.filter(coll_policy=policy_tree_id)
        return query_set

    @staticmethod
    def get_policy_tree_from_db(policy_tree_id):
        obj = CollPolicy.objects.get(coll_policy_id=policy_tree_id)
        return obj





