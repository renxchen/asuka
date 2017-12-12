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
        self.render_b_c = self.instead.join(self.basic_c.split())
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
        basic_character = ''
        extract_data = []
        # if find the basic character, False is not find, True is find.
        basic_c_find_flag = False
        # calculate if match the offset
        count = 0
        result = []
        # find the basic character and replace the basic character as the reconstructed character
        for i in range(len(self.raw_data_list)):
            if self.basic_c in self.raw_data_list[i]:
                self.raw_data_list[i] = self.raw_data_list[i].replace(self.basic_c, self.render_b_c)
        new_list = ''.join(self.raw_data_list).split()
        if self.x_offset < 0:
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
            if new_list[i].isspace():
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
        self.res['basic_character_index'] = result[0]
        # self.res['basic_character'] = ''.join(self.raw_data_list).split()[result[0]].replace(constants.INSTEAD, ' ')
        self.res['basic_character'] = basic_character.replace(constants.INSTEAD, ' ')
        self.res['extract_data_index'] = result[-1]
        # self.res['extract_data'] = ''.join(self.raw_data_list).split()[result[-1]]
        self.res['extract_data'] = extract_data
        return self.res

    def x_offset_comma_extract(self):
        pass

    def x_offset_slash_extract(self):
        pass

    def y_offset_space_extract(self):
        # if find the basic character, False is not find, True is find.
        basic_c_find_flag = False
        # calculate if match the offset
        count = 0
        basic_c_line_num = 0
        basic_c_len = 0
        start_characters = ''
        result = []
        new_list = []
        # destination line num in the raw data
        target_line_num = 0
        new_start_c_list = []
        # find the basic character and replace the basic character to the reconstructed character
        for i in range(len(self.raw_data_list)):
            if self.basic_c in self.raw_data_list[i]:
                basic_c_find_flag = True
                # find the line number that basic character is belong to
                basic_c_line_num = i
                self.raw_data_list[i] = self.raw_data_list[i].replace(self.basic_c, self.render_b_c)
                # destination line num
                target_line_num = basic_c_line_num + self.y_offset
            # find the basic character in destination line.
            if i == target_line_num and basic_c_find_flag and self.y_offset > 0:
                start_characters = self.raw_data_list[i]
                new_list = ''.join(self.raw_data_list[:i]).split()
        if self.y_offset < 0:
            for i in range(len(self.raw_data_list)):
                if i == target_line_num:
                    start_characters = self.raw_data_list[i]
                    new_list = ''.join(self.raw_data_list[:basic_c_line_num + 1]).split()
                    new_start_c_list = ''.join(self.raw_data_list[:target_line_num + 1]).split()

        for i in range(len(new_list)):
            pattern = re.compile(self.render_b_c)
            m = re.search(pattern, new_list[i])
            if m is not None:
                # record the index(position) of the basic character
                result.append(i)
                continue
        start_characters_list = start_characters.split()
        for i in range(len(start_characters_list)):
            if start_characters_list[i].isspace():
                continue
            else:
                count += 1
            # match the offset and should find the extract data
            if count - 1 == int(str(self.x_offset).replace('-', '')):
                pattern = re.compile(self.extract_regexp)
                m = re.search(pattern, start_characters_list[i])
                if m is not None:
                    # record the index(position) of the extract data
                    if self.y_offset > 0:
                        result.append(len(new_list) + i)
                    else:
                        result.append(len(new_start_c_list) -
                                      (len(start_characters_list) - int(str(self.x_offset).replace('-', ''))))
                else:
                    result.append(constants.NO_MATCH_EXTRACT_DATA_REGEXP)
                break
        self.res['basic_character_index'] = result[0]
        self.res['basic_character'] = ''.join(self.raw_data_list).split()[result[0]].replace(constants.INSTEAD, ' ')
        self.res['extract_data_index'] = result[-1]
        self.res['extract_data'] = ''.join(self.raw_data_list).split()[result[-1]]
        return self.res

    def y_offset_comma_extract(self):
        pass

    def y_offset_slash_extract(self):
        pass

    def regexp_extract(self):
        extract_data_index = []
        exp_result = []
        for line in self.raw_data_list:
            pattern = re.compile(self.extract_regexp)
            m = re.search(pattern, line)
            if m is not None:
                exp_result.append(m.group())
        new_list = ''.join(self.raw_data_list).split()
        for i in range(len(new_list)):
            if new_list[i].isspace():
                continue
            if len(exp_result) > 0:
                for per_result in exp_result:
                    if per_result.lower() == new_list[i].lower():
                        extract_data_index.append(i)
            else:
                pass
        self.res['extract_data_index'] = extract_data_index
        return self.res

    def expect_line_or_all_extract(self):
        extract_data_index = []
        new_list = ''.join(self.raw_data_list).split()
        for i in range(len(new_list)):
            if new_list[i].isspace():
                continue
            if i == 0:
                extract_data_index.append(i)
            if i == len(new_list) - 1:
                extract_data_index.append(i)
        self.res['extract_data_index'] = extract_data_index
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
            return self.expect_line_or_all_extract()


def test():
    # data = '''GigabitEthernet0/0/0 is up, line protocol is up
    #               Hardware is 4XGE-BUILT-IN, address is 2c54.2d61.7200 (bia 2c54.2d61.7200)
    #               Internet address is 10.92.51.106/30
    #               MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
    #                  Available Flows     = 70495509
    #                  Received 0 broadcasts (0 IP multicasts)
    # '''
    data = '''ROUTER#show sbc global dbe media-stats
                SBC Service "global"
                Max Term per Context   = 68
                Available Bandwidth    = Unlimited
                Available Flows        = 60786Unlimited66666
                Available Packet Rate  = Unlimited
                Active Media Flows     = 26
                Peak Media Flows       = 66
                Total Media Flows      = 108112
                Active Signaling Flows = 4692
    '''
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
    extract_policy = {
        'rule_type': 1,
        'basic_characters': 'Available Packet Rate',
        'split_characters': 'space',
        'x_offset': -1,
        'y_offset': -3,
        'expect_line_number': 6,
        'extract_regexp': '(\d+)[A-Z][a-z]+(\d+)',
        'start_line': 1,
        'end_line': 6,
        'deep': None,
        'block_start_characters': None,
        'block_end_characters': None,
        'is_include_end_characters': False,
        'block_start_offset': None,
        'block_end_offset': None,
        'is_serial': False

    }
    # input dict
    # extract_policy = {
    #     'rule_type': 1,
    #     'basic_characters': None,
    #     'split_characters': None,
    #     'x_offset': None,
    #     'y_offset': None,
    #     'expect_line_number': None,
    #     'extract_regexp': None,
    #     'start_line': None,
    #     'end_line': None,
    #     'deep': 0,
    #     'block_start_characters': None,
    #     'block_end_characters': None,
    #     'is_include_end_characters': False,
    #     'block_start_offset': None,
    #     'block_end_offset': None,
    #     'is_serial': False
    # }
    d = DataExtractPolicy(data, **extract_policy)
    r = d.dispatch()
    render = Render(**r)
    print render.render()


# test()
