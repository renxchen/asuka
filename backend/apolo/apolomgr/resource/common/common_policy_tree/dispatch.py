#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: dispatch.py
@time: 2017/12/18
@desc:

'''

from backend.apolo.apolomgr.resource.common.common_policy_tree.rule import Policy

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
        the_first_data['block_path'] = ''
        self.instance = Policy(extract_policy=the_first_data)


    def dispatch(self, work_follow_num=0):
        work_follow_num += 1
        if self.work_follow.has_key(work_follow_num):
            func_name = self.work_follow.get(work_follow_num)
            result = getattr(self.instance, func_name)()
            self.buffer_res.append(result)
            # the next work follow
            if self.work_follow.has_key(work_follow_num+1):
                # parent node rule  is block rule with regular and data extract is expect_line_extract
                if len(result)> 0 and result[0]['rule_type']==8 and self.work_follow.get(work_follow_num + 1) == 'expect_line_extract':
                    # set the input of the next method
                    rule_id = self.path[work_follow_num]
                    input_dict = self.rules[rule_id]
                    input_dict['deep'] = work_follow_num
                    input_dict['rule_d_line_num'] = len(result[0]['reg_match_context'])
                    input_dict['start_line'] =result[0]['start_line']
                    input_dict['end_line'] = result[0]['end_line']
                    input_dict['block_path'] = result[0]['block_path']
                    setattr(self.instance, 'extract_policy', input_dict)
                    self.dispatch(work_follow_num)
                else:
                    for pre in result:
                        # set the input of the next method
                        rule_id = self.path[work_follow_num]
                        input_dict = self.rules[rule_id]
                        input_dict['deep'] = work_follow_num
                        input_dict['start_line'] = pre['start_line']
                        input_dict['end_line'] = pre['end_line']
                        input_dict['block_path'] = pre['block_path']
                        setattr(self.instance, 'extract_policy', input_dict)
                        self.dispatch(work_follow_num)
        else:
            return

    def set_work_follow(self):
        work_follow_num = 1
        for rule_id in self.path:
            if self.rules[rule_id]['rule_type'] ==1:
                self.work_follow.update({work_follow_num: "x_offset_extract"})
            elif self.rules[rule_id]['rule_type'] ==2:
                self.work_follow.update({work_follow_num: "y_offset_extract"})
            elif self.rules[rule_id]['rule_type'] == 3:
                self.work_follow.update({work_follow_num: "regexp_extract"})
            elif self.rules[rule_id]['rule_type'] == 4:
                self.work_follow .update({work_follow_num: "expect_line_extract"})
            elif self.rules[rule_id]['rule_type'] ==5:
                self.work_follow.update({work_follow_num: "extract_block_by_indent"})
            elif self.rules[rule_id]['rule_type'] ==6:
                self.work_follow.update({work_follow_num: "extract_block_by_line_num"})
            elif self.rules[rule_id]['rule_type'] == 7:
                self.work_follow.update({work_follow_num: "extract_block_by_string_range"})
            elif self.rules[rule_id]['rule_type'] == 8:
                self.work_follow .update({work_follow_num: "extract_block_by_regular"})
            elif self.rules[rule_id]['rule_type'] == 9:
                self.work_follow .update({work_follow_num: "all_extract"})
            else:
                return {"errorMsg": "the rule type is not exist"}
            work_follow_num +=1

    def get_result(self):
        return self.buffer_res




