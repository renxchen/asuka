#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: extraction_policy.py
@time: 2017/12/14 14:07
@desc:

'''

import re
from backend.apolo.tools import constants
from django.http import HttpResponse
import simplejson as json


class Render(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.data = kwargs['data']
        self.start_line = kwargs['start_line']
        self.end_line = kwargs['end_line']
        self.block_start_characters = kwargs['block_start_characters']
        self.block_end_characters = kwargs['block_end_characters']
        self.basic_character_index = kwargs['basic_character_index']
        self.basic_character = kwargs['basic_character']
        self.extract_data_index = kwargs['extract_data_index']
        self.extract_data = kwargs['extract_data']
        self.colors1 = ["#FDEDEC", "#EBF5FB", "#F5EEF8", "#FEF9E7", "#F8F9F9"]
        self.colors2 = ["#FADBD8", "#D6EAF8", "#EBDEF0", "#FCF3CF", "#F2F3F4"]
        self.colors3 = ["#F5B7B1", "#AED6F1", "#D7BDE2", "#F9E79F", "#E5E7E9"]

    def render(self):
        return self.kwargs
        # return HttpResponse(self.kwargs)


class DataExtractPolicy(object):
    def __init__(self, data, **extract_policy):
        # raw data
        self.data = data
        self.extract_policy = extract_policy
        self.rule_type = extract_policy['rule_type']
        self.start = extract_policy['start_line']
        self.end = extract_policy['end_line']
        self.x_offset = extract_policy['x_offset']
        self.y_offset = extract_policy['y_offset']
        self.split_characters = self.extract_policy['split_characters']
        self.expect_line_number = extract_policy['expect_line_number']
        self.block_start_characters = extract_policy['block_start_characters']
        self.block_end_characters = extract_policy['block_end_characters']
        self.basic_c = extract_policy['basic_characters']
        self.extract_regexp = extract_policy['extract_regexp']
        # raw data of target block
        self.raw_data_list = self.data.split('\n')[self.start:self.end + 1]
        self.instead = constants.INSTEAD
        self.render_b_c = ''
        # return dic
        self.res = {
            'data': self.data,
            'start_line': self.start,  # the starting position of a line
            'end_line': self.end,  # the ending position of a line
            'block_start_characters': self.block_start_characters,  # the starting character of blcok
            'block_end_characters': self.block_end_characters,  # the ending character of blcok
            'basic_character_index': None,  # the basic character position
            'basic_character': None,  # the basic character
            'extract_data_index': None,  # the extract data position
            'extract_data': None  # the extract data
        }

    def x_offset_space_extract(self):
        # the value of basic character
        basic_character = ''
        # the value of extract data
        extract_data = []
        # if find the basic character, False is not find, True is find.
        basic_c_find_flag = False
        # calculate if match the offset
        count = 0
        # record the index(position)
        result = []
        # find the basic character and replace the basic character as the <@@> reconstructed character
        for i in range(len(self.raw_data_list)):
            pattern = re.compile(self.basic_c)
            m = re.search(pattern, self.raw_data_list[i])
            if m is not None:
                basic_character = m.group()
                # replace the space in basic character to @@
                self.render_b_c = self.instead.join(basic_character.split())
                self.raw_data_list[i] = self.raw_data_list[i].replace(basic_character, self.render_b_c)
        # split the raw data that combine by ''
        new_list = ''.join(self.raw_data_list).split(' ')
        if self.x_offset < 0:
            # reverse the list
            new_list.reverse()
        for i in range(len(new_list)):
            pattern = re.compile(self.render_b_c)
            m = re.search(pattern, new_list[i])
            if m is not None:
                basic_character = m.group()
                # find the basic character
                basic_c_find_flag = True
                # record the index(position) of the basic character
                result.append(i)
                continue
            if new_list[i].isspace() or new_list[i] == '':
                continue
            if basic_c_find_flag and new_list[i] is not '':
                count += 1
            # match the offset and should find the extract data
            if count == int(str(self.x_offset).replace('-', '')):
                pattern = re.compile(self.extract_regexp)
                m = re.search(pattern, new_list[i])
                if m is not None:
                    if m.groups():
                        for per_val in m.groups():
                            extract_data.append(per_val)
                    else:
                        extract_data = m.group()
                    # record the index(position) of the extract data
                    result.append(i)
                else:
                    result.append(constants.NO_MATCH_EXTRACT_DATA_REGEXP)
                break
        if self.x_offset < 0:
            result = [len(new_list) - 1 - result[0],
                      result[-1] if isinstance(result[-1], str) else len(new_list) - 1 - result[-1]]
        # the position of basic character
        self.res['basic_character_index'] = result[0]
        # the value of basic character
        self.res['basic_character'] = basic_character.replace(constants.INSTEAD, ' ')
        # the position of extract data
        self.res['extract_data_index'] = result[-1]
        # the value of extract data
        self.res['extract_data'] = extract_data
        # print ''.join(self.raw_data_list).split(' ')[38]
        # print ''.join(self.raw_data_list).split(' ')[22]
        return self.res

    def x_offset_comma_extract(self):
        pass

    def x_offset_slash_extract(self):
        pass

    def y_offset_space_extract(self):
        # if find the basic character, False is not find, True is find.
        basic_character_line_find_flag = False
        # calculate if match the offset
        count = 0
        basic_character_find_flag = False
        # value of basic character
        basic_character = ''
        # value of extract data
        extract_data = []
        # the line number of the basic character belong
        basic_character_line_num = 0
        start_characters_line = ''
        result = []
        new_list = []
        # destination line num in the raw data
        target_line_num = 0
        new_start_character_list = []
        # new_list = ''.join(self.raw_data_list).split(' ')
        # find the basic character and replace the basic character to the reconstructed character
        for i in range(len(self.raw_data_list)):
            pattern = re.compile(self.basic_c)
            m = re.search(pattern, self.raw_data_list[i])
            if m is not None:
                basic_character = m.group()
                # find the line that basic character
                basic_character_line_find_flag = True
                # find the line number for the basic character
                basic_character_line_num = i
                self.render_b_c = self.instead.join(basic_character.split())
                # replace the space in basic character to @@
                self.raw_data_list[i] = self.raw_data_list[i].replace(basic_character, self.render_b_c)
                # destination line num
                target_line_num = basic_character_line_num + self.y_offset
            # find the basic character in destination line.
            if self.y_offset > 0:
                if basic_character_line_find_flag:
                    if i == target_line_num:
                        start_characters_line = self.raw_data_list[i]
                        new_list = ''.join(self.raw_data_list[:target_line_num]).split(' ')
        if self.y_offset < 0:
            for i in range(len(self.raw_data_list)):
                if i == target_line_num:
                    start_characters_line = self.raw_data_list[i]
                    new_list = ''.join(self.raw_data_list[:basic_character_line_num + 1]).split(' ')
                    new_start_character_list = ''.join(self.raw_data_list[:target_line_num + 1]).split(' ')
        # find the basic character
        for i in range(len(new_list)):
            pattern = re.compile(self.render_b_c)
            m = re.search(pattern, new_list[i])
            if m is not None:
                basic_character = m.group()
                # find the basic character
                basic_character_find_flag = True
                # record the index(position) of the basic character
                result.append(i)
                break
        start_characters_list = start_characters_line.split(' ')
        for i in range(len(start_characters_list)):
            if start_characters_list[i].isspace() or start_characters_list[i] == '':
                continue
            count += 1
            # match the offset and should find the extract data
            if count - 1 == int(str(self.x_offset).replace('-', '')):
                pattern = re.compile(self.extract_regexp)
                m = re.search(pattern, start_characters_list[i])
                if m is not None:
                    if m.groups():
                        for per_val in m.groups():
                            extract_data.append(per_val)
                    else:
                        extract_data = m.group()
                    # record the index(position) of the extract data
                    if self.y_offset > 0:
                        result.append(len(new_list) - 1 + i)
                    else:
                        result.append(len(new_start_character_list) - len(start_characters_list) + i)
                else:
                    result.append(constants.NO_MATCH_EXTRACT_DATA_REGEXP)
                break
        self.res['basic_character_index'] = result[0]
        self.res['extract_data_index'] = result[-1]
        self.res['basic_character'] = basic_character.replace(constants.INSTEAD, ' ')
        self.res['extract_data'] = extract_data
        # print ''.join(self.raw_data_list).split(' ')[83]
        # print ''.join(self.raw_data_list).split(' ')[67]
        # for j in range(len(''.join(self.raw_data_list).split(' '))):
        #     print j, ' ==== ', ''.join(self.raw_data_list).split(' ')[j]
        return self.res

    def y_offset_comma_extract(self):
        pass

    def y_offset_slash_extract(self):
        pass

    def regexp_extract(self):
        extract_data_index = []
        exp_result = []
        # value of extract data
        extract_data = []
        for line in self.raw_data_list:
            pattern = re.compile(self.extract_regexp)
            m = re.search(pattern, line)
            if m is not None:
                extract_data.append(line)
                exp_result.append(m.group())
        new_list = ''.join(self.raw_data_list).split(' ')
        for i in range(len(new_list)):
            if new_list[i].isspace() or new_list[i] == '':
                continue
            if len(exp_result) > 0:
                for per_result in exp_result:
                    if per_result.lower() == new_list[i].lower():
                        extract_data_index.append(i)
            else:
                extract_data_index.append(constants.NO_MATCH_EXTRACT_DATA_REGEXP)
        self.res['extract_data_index'] = extract_data_index
        self.res['extract_data'] = extract_data
        return self.res

    def expect_line_extract(self):
        extract_data_index = []
        new_list = ''.join(self.raw_data_list).split(' ')
        for i in range(len(new_list)):
            if new_list[i].isspace() or new_list[i] == '':
                continue
            if i == 0:
                extract_data_index.append(i)
            if i == len(new_list) - 1:
                extract_data_index.append(i)
        self.res['extract_data_index'] = extract_data_index
        return self.res

    def all_extract(self):
        extract_data_index = []
        new_list = ''.join(self.raw_data_list).split(' ')
        for i in range(len(new_list)):
            if new_list[i].isspace() or new_list[i] == '':
                continue
            else:
                first_character_flag = True
                first_character_index = i
            if first_character_flag:
                extract_data_index.append(first_character_index)
                break
        for i in range(len(new_list)):
            if new_list[len(new_list) - 1 - i].isspace() or new_list[len(new_list) - 1 - i] == '':
                continue
            else:
                last_character_flag = True
                last_character_index = len(new_list) - 1 - i
            if last_character_flag:
                extract_data_index.append(last_character_index)
                break
        self.res['extract_data_index'] = extract_data_index
        print new_list[0]
        print new_list[209]
        return self.res

    def dispatch(self):
        # 1: x_offset_space_extract, 2:y_offset_space_extract, 3:regexp_extract,4:expect_line_or_all_extract
        if self.rule_type == 1:
            return self.x_offset_space_extract()
        if self.rule_type == 2:
            return self.y_offset_space_extract()
        if self.rule_type == 3:
            return self.regexp_extract()
        if self.rule_type == 4:
            return self.expect_line_extract()
        if self.rule_type == 5:
            return self.all_extract()


def test():
    # data = '''GigabitEthernet0/0/0 is up, line protocol is up
    #               Hardware is 4XGE-BUILT-IN, address is 2c54.2d61.7200 (bia 2c54.2d61.7200)
    #               Internet address is 10.92.51.106/30
    #               MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
    #                  Available Flows     = 70495509
    #                  Received 0 broadcasts (0 IP multicasts)
    # '''
    # data = '''ROUTER#dir harddisk:
    #             278536  -rw-     3832112   Aug 5 2016 14:34:58 +09:00  asr1000-rommon.154-2r.S.pkg
    #             278537  -rw-     1255728   Aug 8 2016 22:29:22 +09:00  asr1000-rommon.122-33r.XND1.pkg
    #             278538  -rw-     4160464   Aug 8 2016 22:38:03 +09:00  asr1000-rommon.162-1r.pkg
    #             180227  -rw-        7838  Sep 20 2016 17:39:49 +00:00  packages.conf
    # '''
    # data = '''sh int port-channel
    #         FF3E::9800:0                            Port-channel4.1866 00:10:25  not used
    #         FF3E::9800:0                            Port-channel4.3433 3d19h     not used
    #         FF3E::9800:0                            Port-channel4.3810 1w3d      not used
    #         FF3E::9800:200                          Port-channel1.1204 1w3d      not used
    #         FF3E::9800:0                            Port-channel1.1260 00:39:20  not used
    #         FF3E::9800:0                            Port-channel1.1325 1d22h     not used
    #         FF3E::9800:0                            Port-channel1.1339 10:11:51  not used
    # '''
    # data = '''ROUTER#show run
    #             Building configuration...
    #
    #             Current configuration : 4174 bytes
    #             !
    #             version 12.2
    #             service timestamps debug datetime msec1
    #             service timestamps log datetime msec
    #             platform shell
    # '''
    data = '''ROUTER#show sbc global dbe media-stats
                SBC Service "global"
                Max Term per Context   = 682
                Available Bandwidth    = Unlimited
                Available Flows        = 60786Unlimited66666
                Available Packet Rate  = Unlimited
                Active Media Flows     = 261
                Peak Media Flows       = 66
                Total Media Flows      = 1081121111
                Active Signaling Flows = 4692
    '''
    extract_policy = {
        'rule_type': 5,
        'basic_characters': 'Available Flows',
        'split_characters': 'space',
        'x_offset': 3,
        'y_offset': -100,
        'expect_line_number': 3,
        'extract_regexp': 'asr.*pkg',
        # 'extract_regexp': '\d+',
        'start_line': 0,
        'end_line': 100,
        'deep': None,
        'block_start_characters': None,
        'block_end_characters': None,
        'is_include_end_characters': False,
        'block_start_offset': None,
        'block_end_offset': None,
        'is_serial': False

    }
    d = DataExtractPolicy(data, **extract_policy)
    r = d.dispatch()
    render = Render(**r)
    print render.render()


test()
