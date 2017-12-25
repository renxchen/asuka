#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: dispatch.py
@time: 2017/12/18
@desc:

'''

from rule import Policy

class Dispatch(object):

    def __init__(self, path, rules, first_rule_data):
        self.instance = Policy(extract_policy=first_rule_data)
        # path is that is from root node to leaf node .
        # for example :[(tree id of root,rule id of root),..,(tree id of leaf,rule id of leaf)]
        self.path = path
        # {tree_id,rule_context}
        self.rules = rules
        self.buffer_res = []
        self.work_follow = {}
        self.set_work_follow()

    def dispatch(self, work_follow_num=0):
        work_follow_num += 1
        if self.work_follow.has_key(work_follow_num):
            func_name = self.work_follow.get(work_follow_num)
            result = getattr(self.instance, func_name)()
            self.buffer_res.append(result)
            # the next work follow
            if self.work_follow.has_key(work_follow_num+1):
                for pre in result:
                    # set the input of the next method
                    tree_id = self.path[work_follow_num][0]
                    input_dict = self.rules[tree_id]
                    input_dict['deep'] = work_follow_num
                    input_dict['start_line'] = pre['start_line']
                    input_dict['end_line'] = pre['end_line']
                    setattr(self.instance, 'extract_policy', input_dict)
                    self.dispatch(work_follow_num)
        else:
            return

    def set_work_follow(self):
        work_follow_num = 1
        for item in self.path:
            tree_id = item[0]
            if self.rules[tree_id]['rule_type'] ==1:
                self.work_follow.update({work_follow_num: "x_offset_space_extract"})
            elif self.rules[tree_id]['rule_type'] ==2:
                self.work_follow.update({work_follow_num: "y_offset_space_extract"})
            elif self.rules[tree_id]['rule_type'] == 3:
                self.work_follow.update({work_follow_num: "regexp_extract"})
            elif self.rules[tree_id]['rule_type'] == 4:
                self.work_follow .update({work_follow_num: "expect_line_or_all_extract"})
            elif self.rules[tree_id]['rule_type'] ==5:
                self.work_follow.update({work_follow_num: "extract_block_by_indent"})
            elif self.rules[tree_id]['rule_type'] ==6:
                self.work_follow.update({work_follow_num: "extract_block_by_line_num"})
            elif self.rules[tree_id]['rule_type'] == 7:
                self.work_follow.update({work_follow_num: "extract_block_by_string_range"})
            elif self.rules[tree_id]['rule_type'] == 8:
                self.work_follow .update({work_follow_num: "extract_block_by_regular"})
            else:
                return {"errorMsg": "the rule type is not exist"}
            work_follow_num +=1

    def get_result(self):
        return self.buffer_res




