#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: tool.py
@time: 2018/1/4 15:14
@desc:

'''
import constants


class Tool(object):

    @staticmethod
    def set_split_char(split_char_num=None):

        if split_char_num == 0:
            split_char = constants.SPLIT_RULE_SPACE
        elif split_char_num == 1:
            split_char = constants.SPLIT_RULE_COMMA
        elif split_char_num == 2:
            split_char = constants.SPLIT_RULE_SLASH
        elif split_char_num == 3:
            split_char = constants.SPLIT_RULE_OTHER
        else:
            split_char = ''

        return split_char

    def get_rule_value(self, obj):
        split_char = self.set_split_char(obj['split_char'])
        input_data_dict = {'rule_type': obj['rule_type'],
                           'basic_characters': obj['mark_string'],
                           'split_characters': split_char,
                           'x_offset': obj['x_offset'],
                           'y_offset': obj['y_offset'],
                           'expect_line_number': obj['line_nums'],
                           'extract_regexp': obj['extract_key'],
                           'start_line': None,
                           'end_line': None,
                           'deep': 0,
                           'block_start_characters': obj['mark_string'],
                           'block_end_characters': obj['end_mark_string'],
                           'is_include_end_characters': obj['is_include'],
                           'is_serial': obj['is_serial'],
                           'block_start_offset': obj['start_line_num'],
                           'block_end_offset': obj['end_line_num']
                           }
        return input_data_dict
