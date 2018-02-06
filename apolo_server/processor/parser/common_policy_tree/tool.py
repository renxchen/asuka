#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: tool.py
@time: 2018/1/4 15:14
@desc:

'''
import json
import time

import requests

from backend.apolo.tools import constants


class Tool(object):
    @staticmethod
    def set_rule_type(rule_type):
        if rule_type>=5:
            rule_type = rule_type - 4
            return 'block_rule_{}'.format(rule_type)
        else:
            return 'data_rule_{}'.format(rule_type)

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
        #split_char = self.set_split_char(obj.split_char)
        input_data_dict = {'rule_type': obj['rule_type'],
                           'basic_characters': obj['mark_string'],
                           'split_characters': obj['split_char'],
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

    @staticmethod
    def split_data_schedule_time(data_schedule_time):

        if data_schedule_time:
            schedule_arry = data_schedule_time.split('@')
            weeks = schedule_arry[0].split(';')
            schedule_time = schedule_arry[1].split('-')
            schedule_start_time = schedule_time[0]
            schedule_end_time = schedule_time[1]

            return {'weeks': weeks,
                    'schedule_start_time': schedule_start_time,
                    'schedule_end_time': schedule_end_time
                    }
        else:
            return {'weeks': [],
                    'schedule_start_time': '00:00',
                    'schedule_end_time': '00:00'
                    }

    @staticmethod
    def priority_mapping(priority_key):
        levels = [{constants.PRIORITY_HIGH_LEVEL_KEY: constants.PRIORITY_HIGH_LEVEL_VALUE},
                  {constants.PRIORITY_STANDARD_LEVEL_KEY: constants.PRIORITY_STANDARD_LEVEL_VALUE},
                  {constants.PRIORITY_URGENT_LEVEL_KEY: constants.PRIORITY_URGENT_LEVEL_VALUE}]
        level_value = []
        for item in levels:
            if priority_key in item.keys()[0]:
                level_value.append(item.values()[0])
        return level_value

    @staticmethod
    def schedule_type_mapping(schedule_type_key):
        levels = [{constants.SCHEDULE_TYPE_OFTEN_KEY: constants.SCHEDULE_TYPE_OFTEN_VALUE},
                  {constants.SCHEDULE_TYPE_STOP_KEY: constants.SCHEDULE_TYPE_STOP_VALUE},
                  {constants.SCHEDULE_TYPE_PERIOD_KEY: constants.SCHEDULE_TYPE_PERIOD_VALUE}]
        level_value = []
        for item in levels:
            if schedule_type_key in item.keys()[0]:
                level_value.append(item.values()[0])

        return level_value

    @staticmethod
    def schedule_status_mapping(schedule_status_key):
        levels = [{constants.SCHEDULE_STATUS_ON_KEY: constants.SCHEDULE_STATUS_ON_VALUE},
                  {constants.SCHEDULE_STATUS_OFF_KEY: constants.SCHEDULE_STATUS_OFF_VALUE}
                ]
        level_value = []
        for item in levels:
            if schedule_status_key in item.keys()[0]:
                level_value.append(item.values()[0])

        return level_value

    @staticmethod
    def set_priority_mapping(priority_value):
        if priority_value == constants.PRIORITY_HIGH_LEVEL_VALUE:
            return constants.PRIORITY_HIGH_LEVEL_KEY
        elif priority_value == constants.PRIORITY_URGENT_LEVEL_VALUE:
            return constants.PRIORITY_URGENT_LEVEL_KEY
        elif priority_value == constants.PRIORITY_STANDARD_LEVEL_VALUE:
            return constants.PRIORITY_STANDARD_LEVEL_KEY
        else:
            return 'ERROR'

    @staticmethod
    def set_cp_status_mapping(cp_status_value):
        if cp_status_value == constants.CP_STATUS_OFF_VALUE:
            return constants.CP_STATUS_OFF_KEY
        elif cp_status_value == constants.CP_STATUS_ON_VAULE:
            return constants.CP_STATUS_ON_KEY
        else:
            return 'ERROR'

    @staticmethod
    def get_data_from_collection_server():
        now_time = int(time.time())
        print now_time
        json_data = json.dumps({"now_time": now_time, "item_type": -1})
        response = requests.post(constants.DATA_COLLECTION_POST_URL, data=json_data)
        return response.json()

if __name__ == '__main__':
    t = Tool()
    t.get_data_from_collection_server()

