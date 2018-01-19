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

    def __init__(self, path, rules, raw_data):

        self.raw_data = raw_data
        self.instance = None
        # path is that is from root node to leaf node .
        # for example :[rule id of root,..,rule id of leaf]
        self.path = path
        # {rule_id:rule_context,...,}
        self.rules = rules
        self.buffer_res = []
        self.work_follow = {}

        self.__set_instance__()

        self.set_work_follow()

    def __set_instance__(self):

        the_first_data = self.rules[self.path[0]]
        # set the init data
        the_first_data['data'] = self.raw_data
        the_first_data['start_line'] = 0
        the_first_data['end_line'] = len(self.raw_data.split('\n'))-1
        self.instance = Policy(extract_policy=the_first_data)

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
                    rule_id = self.path[work_follow_num]
                    input_dict = self.rules[rule_id]
                    input_dict['deep'] = work_follow_num
                    input_dict['start_line'] = pre['start_line']
                    input_dict['end_line'] = pre['end_line']
                    setattr(self.instance, 'extract_policy', input_dict)
                    self.dispatch(work_follow_num)
        else:
            return

    def set_work_follow(self):
        work_follow_num = 1
        for rule_id in self.path:
            if self.rules[rule_id]['rule_type'] ==1:
                self.work_follow.update({work_follow_num: "x_offset_space_extract"})
            elif self.rules[rule_id]['rule_type'] ==2:
                self.work_follow.update({work_follow_num: "y_offset_space_extract"})
            elif self.rules[rule_id]['rule_type'] == 3:
                self.work_follow.update({work_follow_num: "regexp_extract"})
            elif self.rules[rule_id]['rule_type'] == 4:
                self.work_follow .update({work_follow_num: "expect_line_or_all_extract"})
            elif self.rules[rule_id]['rule_type'] ==5:
                self.work_follow.update({work_follow_num: "extract_block_by_indent"})
            elif self.rules[rule_id]['rule_type'] ==6:
                self.work_follow.update({work_follow_num: "extract_block_by_line_num"})
            elif self.rules[rule_id]['rule_type'] == 7:
                self.work_follow.update({work_follow_num: "extract_block_by_string_range"})
            elif self.rules[rule_id]['rule_type'] == 8:
                self.work_follow .update({work_follow_num: "extract_block_by_regular"})
            else:
                return {"errorMsg": "the rule type is not exist"}
            work_follow_num +=1

    def get_result(self):
        return self.buffer_res




