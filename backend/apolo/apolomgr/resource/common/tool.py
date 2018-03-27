#!/usr/bin/env python

"""
@author: kimli
@contact: kimli@cisco.com
@file: tool.py
@time: 2018/1/4 15:14
@desc:
"""
import json
import time
import requests

from backend.apolo.apolomgr.resource.collection_validate.collection_validate import GetValidItem, GetValidItemByPolicy
from backend.apolo.tools import constants


class Tool(object):
    @staticmethod
    def set_rule_type(rule_type):
        """!@brief
        set rule type
        @param rule_type:rule type
        @pre
        @post
        @note all extract data rule type is 9
        @return rule type
        @author kimli
        @date 2018/1/4
        """
        if rule_type >= 5 and rule_type != 9:
            rule_type = rule_type - 4
            return 'block_rule_{}'.format(rule_type)
        else:
            return 'data_rule_{}'.format(rule_type)

    @staticmethod
    def set_split_char(split_char_num=None):
        """!@brief
        replace split char
        @param split_char_num : number corresponding to  kind of split
        @pre
        @post
        @note
        @return split char
        @author kimli
        @date 2018/1/4
        """
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

    @staticmethod
    def get_rule_value(obj):
        """!@brief
        set rule info to dict
        @param
        @pre
        @post
        @note
        @return rule info that value type is dict
        @author kimli
        @date 2018/1/4
        """
        input_data_dict = {'rule_type': obj.rule_type,
                           'basic_characters': obj.mark_string,
                           'split_characters': obj.split_char,
                           'x_offset': obj.x_offset,
                           'y_offset': obj.y_offset,
                           'expect_line_number': obj.line_nums,
                           'extract_regexp': obj.extract_key,
                           'start_line': None,
                           'end_line': None,
                           'deep': 0,
                           'block_start_characters': obj.mark_string,
                           'block_end_characters': obj.end_mark_string,
                           'is_include_end_characters': obj.is_include,
                           'is_serial': obj.is_serial,
                           'block_start_offset': obj.start_line_num,
                           'block_end_offset': obj.end_line_num
                           }
        return input_data_dict

    @staticmethod
    def split_data_schedule_time(data_schedule_time):
        """!@brief
        extract week,schedule_start_time,schedule_end_time from schedule time
        @param
        @pre
        @post
        @note
        @return return week,schedule_start_time,schedule_end_time
        @author kimli
        @date 2018/1/4
        """
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
        """!@brief
        priority mapping function
        @param priority_key: priority key
        @pre
        @post
        @note
        @return priority value list corresponding to priority key
        @author kimli
        @date 2018/1/4
        """
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
        """!@brief
        schedule type  mapping function
        @param schedule_type_key: schedule type key
        @pre
        @post
        @note
        @return schedule typ value list corresponding to schedule type key
        @author kimli
        @date 2018/1/4
        """
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
        """!@brief
        schedule status  mapping function
        @param schedule_status_key: schedule status key
        @pre
        @post
        @note
        @return schedule status value list corresponding to schedule status key
        @author kimli
        @date 2018/1/4
        """
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
        """!@brief
        priority value mapping function
        @param priority_value: priority value
        @pre
        @post
        @note
        @return priority key  corresponding to priority value
        @author kimli
        @date 2018/1/4
        """
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
        """!@brief
        cp status mapping function
        @param cp_status_value: cp status value
        @pre
        @post
        @note
        @return cp status key corresponding to cp status value
        @author kimli
        @date 2018/1/4
        """
        if cp_status_value == constants.CP_STATUS_OFF_VALUE:
            return constants.CP_STATUS_OFF_KEY
        elif cp_status_value == constants.CP_STATUS_ON_VAULE:
            return constants.CP_STATUS_ON_KEY
        else:
            return 'ERROR'

    @staticmethod
    def get_data_from_collection_server():
        """!@brief
        get items that are running
        @param
        @pre
        @post
        @note
        @return return json data of items that are running
        @author kimli
        @date 2018/1/4
        """
        test_instance = GetValidItem()
        valid_items = test_instance.valid(int(time.time()))
        items = map(Tool.__item_type_mapping, valid_items)
        tmp_key_dict = dict()
        result = []
        for recoder in items:
            if tmp_key_dict.has_key(recoder['item_key']):
                pass
            else:
                result.append(recoder)
                tmp_key_dict.update({recoder['item_key']: 1})

        return result

    @staticmethod
    def __item_type_mapping(item):


        def common(item):
            tmp_item = {}
            tmp_item['valid_status'] = item['valid_status']
            tmp_item['policy_group_id'] = item['policys_groups__policy_group_id']
            tmp_item['policy_group_name'] = item['policys_groups__policy_group_id__name']
            tmp_item['coll_policy_id'] = item['coll_policy_id']
            tmp_item['item_id'] = item['item_id']
            tmp_item['item_type'] = item['item_type']
            tmp_item['device_id'] = item['device__device_id']
            tmp_item['priority'] = item['schedule__priority']
            tmp_item['device_name'] = item['device__hostname']
            tmp_item['policy_name'] = item['coll_policy__name']
            tmp_item['exec_interval'] = item['policys_groups__exec_interval']
            tmp_item['item_key']= '{}_{}_{}_{}'.format(tmp_item['policy_group_id'],
                                                    tmp_item['priority'],
                                                    tmp_item['coll_policy_id'],
                                                       tmp_item['device_id'])

            return tmp_item



        result = common(item)
        return result

    @staticmethod
    def get_policy_status(policy_id):
        """!@brief
        get cp status
        @param policy_id:collection policy id
        @pre
        @post
        @note
        @return return cp status. if cp is running,return True.if cp is not running,return False
        @author kimli
        @date 2018/1/4
        """
        test_instance = GetValidItemByPolicy()
        item_num = test_instance.valid(int(time.time()), policy_id)
        if item_num == 0:
            # not used
            return False
        else:
            # is being used
            return True

    @staticmethod
    def replace_escape_char(escapeString):
        """!@brief
        replace special char to general char
        @param escapeString :the char to be replaced
        @pre
        @post
        @note
        @return replaced char
        @author kimli
        @date 2018/1/4
        """
        fbsArr = ["\\", "$", "(", ")", "*", "+", ".", "[", "]", "?", "^", "{", "}", "|"]
        arry = list(escapeString)
        for i in range(len(arry)):
            if arry[i] in fbsArr:
                arry[i] = arry[i].replace(arry[i], '\\' + arry[i])

        return "".join(arry)

    @staticmethod
    def replace_xml_mark(xmlString):
        """!@brief
        replace '<' and '>' to '&lt;' and '&lt;'  when rend highlight html
        @param xmlString :  text that include xml mark
        @pre
        @post
        @note
        @return text to be replaced
        @author kimli
        @date 2018/1/4
        """
        if xmlString:
            if '<' in xmlString and '>' in xmlString:
                xmlString = xmlString.replace('<', '&lt;')
                xmlString = xmlString.replace('>', '&lt;')
        return xmlString


