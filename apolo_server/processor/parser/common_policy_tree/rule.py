#!/usr/bin/env python


'''

@author: kimli
@contact: kimli@cisco.com
@file: rule.py
@time: 2017/12/18
@desc:

'''
import re
from backend.apolo.tools import constants


class Policy(object):
    def __init__(self, extract_policy):
        # self.data = data
        self.extract_policy = extract_policy
        self.data = extract_policy['data']


    def __set_input__(self):

        # self.data = self.extract_policy['data']
        self.start_line = self.extract_policy['start_line']
        self.end_line = self.extract_policy['end_line']
        self.x_offset = self.extract_policy['x_offset']
        self.y_offset = self.extract_policy['y_offset']
        if self.extract_policy['split_characters'] =='@space@':
            self.split_characters = ' '
        else:
            self.split_characters = self.extract_policy['split_characters']
        self.expect_line_number = self.extract_policy['expect_line_number']
        self.block_start_characters = self.extract_policy['block_start_characters']
        self.block_end_characters = self.extract_policy['block_end_characters']
        self.deep = self.extract_policy['deep']
        self.rule_type = self.extract_policy['rule_type']
        self.is_include_end_characters = self.extract_policy['is_include_end_characters']
        self.block_start_offset = self.extract_policy['block_start_offset']
        self.block_end_offset = self.extract_policy['block_end_offset']
        self.is_serial = self.extract_policy['is_serial']
        self.basic_c = self.extract_policy['basic_characters']
        self.extract_regexp = self.extract_policy['extract_regexp']
        # raw data of target block
        if self.deep >0 and self.rule_type >4:
            self.start_line +=1
        self.raw_data_list = self.data.split('\n')[self.start_line:self.end_line + 1]
        self.instead = constants.INSTEAD
        self.render_b_c = ''
        # data extraction's result
        self.block_path = self.extract_policy['block_path']
        self.res = {
            'start_line': self.start_line,  # the starting position of a line
            'end_line': self.end_line,  # the ending position of a line
            'block_start_characters': self.block_start_characters,  # the starting character of block
            'block_end_characters': self.block_end_characters,  # the ending character of block
            'basic_character_index': None,  # the basic character position
            'basic_character': None,  # the basic character
            'extract_data_index': None,  # the extract data position
            'extract_data': None,  # the extract data
            'deep': self.deep,
            'isleaf': True,
            'rule_type': self.rule_type,
            'basic_character_line_num': None,
            'split_characters': self.split_characters,
            'extract_match_flag': False,
            'block_path': None
        }


    def __set_block_path__(self, identifier):

        if self.block_path:
            return '{},{}'.format(self.block_path, identifier)
        else:
            return identifier

    def x_offset_extract(self):

        self.__set_input__()
        # the value of basic character
        basic_character = ''
        # the value of extract data
        extract_data = []
        # if find the basic character, False is not find, True is find.
        basic_c_find_flag = False
        # calculate if match the offset
        count = 0
        # the line number of basic character
        basic_character_line_num = None
        # the index of basic character
        basic_character_index = None
        # the flag of data whether are extracted. True is extracted,False is not extracted
        extract_data_match_flag = False
        # error message
        msg = ''
        # extract data index
        extract_data_index = None
        # find the basic character and replace the basic character as the <@@> reconstructed character
        for i in range(len(self.raw_data_list)):
            pattern = re.compile(self.basic_c)
            m = re.search(pattern, self.raw_data_list[i])
            if m is not None:
                basic_character = m.group()
                # replace the space in basic character to @@
                self.render_b_c = self.instead.join(basic_character.split())
                self.raw_data_list[i] = self.raw_data_list[i].replace(basic_character, self.render_b_c)
                basic_character_line_num = i
                break
        new_list = []
        for arry in self.raw_data_list:
            new_list.extend(re.split(self.split_characters, arry))

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
                basic_character_index = i
                continue
            if new_list[i].isspace() or new_list[i] == '':
                continue
            if basic_c_find_flag and new_list[i] is not '':
                count += 1
            # match the offset and should find the extract data
            if count == abs(self.x_offset):
                pattern = re.compile(self.extract_regexp)
                m = re.search(pattern, new_list[i])
                if m is not None:
                    extract_data_match_flag = True
                    d = m.group()
                    extract_data.append(d)
                    extract_data_index = i
                else:
                    msg = constants.NO_MATCH_EXTRACT_DATA_REGEXP
                break
        if count < abs(self.x_offset):
            msg = constants.OFFSET_ERROR

        if extract_data_match_flag:

            if self.x_offset < 0:
                basic_character_index = len(new_list) - 1 - basic_character_index
                extract_data_index = len(new_list) - 1 - extract_data_index

            # the line number of basic character
            self.res['basic_character_line_num'] = basic_character_line_num
            # the position of basic character
            self.res['basic_character_index'] = basic_character_index
            # the value of basic character
            self.res['basic_character'] = basic_character.replace(constants.INSTEAD, self.split_characters)
            # the pair of extract data and the position of extract data
            self.res['extract_data_result'] = [(extract_data_index, extract_data[0])]
            # the value of extract data
            self.res['extract_data'] = extract_data
            # the flag of extract data whether is success.True = success ,False = fail
            self.res['extract_match_flag'] = extract_data_match_flag
            # error message
            self.res['error_msg'] = msg
            # block rule path
            self.res['block_path'] = self.block_path
        else:
            self.res['extract_data'] = extract_data
            self.res['extract_match_flag'] = extract_data_match_flag
            self.res['error_msg'] = msg
        return [self.res]

    def y_offset_space_extract_bk(self):
        self.__set_input__()
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
        extract_data_match_flag = False
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
                        new_list = '\n'.join(self.raw_data_list[:target_line_num]).split(' ')
        if self.y_offset < 0:
            for i in range(len(self.raw_data_list)):
                if i == target_line_num:
                    start_characters_line = self.raw_data_list[i]
                    new_list = '\n'.join(self.raw_data_list[:basic_character_line_num + 1]).split(' ')
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
                    extract_data_match_flag = True
                else:
                    result.append(constants.NO_MATCH_EXTRACT_DATA_REGEXP)
                break
        if extract_data_match_flag:
            self.res['basic_character_index'] = result[0]
            self.res['extract_data_index'] = result[-1]
            self.res['basic_character'] = basic_character.replace(constants.INSTEAD, ' ')
            self.res['extract_data'] = extract_data
            self.res['basic_character_line_num'] = basic_character_line_num
            self.res['extract_match_flag'] = True
            # print ''.join(self.raw_data_list).split(' ')[83]
            # print ''.join(self.raw_data_list).split(' ')[67]
            # for j in range(len(''.join(self.raw_data_list).split(' '))):
            #     print j, ' ==== ', ''.join(self.raw_data_list).split(' ')[j]
        return [self.res]

    def y_offset_extract(self):
        self.__set_input__()
        # the line number of the basic character belong
        basic_character_line_num = None
        # value of basic character
        basic_character = ''
        # index of basic character
        basic_character_index = None
        # value of extract data
        extract_data = []
        # the index of extract data
        extract_data_index = None
        # destination line num in the raw data
        extract_data_match_flag = False
        # error message
        msg = None
        target_line_num = None

        # find the basic character and replace the basic character to the reconstructed character
        for i in range(len(self.raw_data_list)):
            pattern = re.compile(self.basic_c)
            m = re.search(pattern, self.raw_data_list[i])
            if m is not None:
                basic_character = m.group()
                # find the line number for the basic character
                basic_character_line_num = i
                self.render_b_c = basic_character.replace(self.split_characters, self.instead)
                # replace the space in basic character to @@
                self.raw_data_list[i] = self.raw_data_list[i].replace(basic_character, self.render_b_c)
                # destination line num
                target_line_num = basic_character_line_num + self.y_offset
                if target_line_num > len(self.raw_data_list) or target_line_num < 0:
                    self.res['extract_match_flag'] = False
                    self.res['error_msg'] = constants.OFFSET_ERROR
                    return self.res

        sum_count = 0
        element_count = -1
        is_start_count = False
        match_count = 0
        basic_character_find_flag = False

        for i in range(len(self.raw_data_list)):
            one_line = self.raw_data_list[i]
            arry = re.split(self.split_characters, one_line)
            if i == target_line_num:
                is_start_count = True
            for j in range(len(arry)):
                if arry[j].isspace() or arry[j] == '':
                    sum_count += 1
                    continue
                if is_start_count:
                    element_count +=1
                if element_count == self.x_offset and is_start_count:
                    match_count +=1
                    is_start_count = False
                    extract_patt = re.compile(self.extract_regexp)
                    m = re.search(extract_patt, arry[j])
                    extract_data_index = sum_count
                    if m is not None:
                        extract_data.append(m.group())
                        extract_data_match_flag = True
                    else:
                        msg = constants.NO_MATCH_EXTRACT_DATA_REGEXP

                if i == basic_character_line_num and not basic_character_find_flag:
                    pattern = re.compile(self.render_b_c)
                    m = re.search(pattern, arry[j])
                    if m is not None:
                        match_count += 1
                        basic_character = m.group()
                        # find the basic character
                        basic_character_find_flag = True
                        # record the index(position) of the basic character
                        basic_character_index = sum_count
                if match_count == 2:
                    break
                sum_count +=1

        if element_count < self.x_offset:
            msg = constants.OFFSET_ERROR

        if extract_data_match_flag:
            # the line number of basic character
            self.res['basic_character_line_num'] = basic_character_line_num
            # the position of basic character
            self.res['basic_character_index'] = basic_character_index
            # the value of basic character
            self.res['basic_character'] = basic_character.replace(constants.INSTEAD, self.split_characters)
            # the pair of extract data and the position of extract data
            self.res['extract_data_result'] = [(extract_data_index, extract_data[0])]
            # the value of extract data
            self.res['extract_data'] = extract_data
            # the flag of extract data whether is success.True = success ,False = fail
            self.res['extract_match_flag'] = extract_data_match_flag
            # error message
            self.res['error_msg'] = msg
            # block rule path
            self.res['block_rule_path'] = ''
        else:
            self.res['extract_data'] = extract_data
            self.res['extract_match_flag'] = extract_data_match_flag
            self.res['error_msg'] = msg
        return [self.res]


    def regexp_extract(self):
        self.__set_input__()
        exp_result = []
        # value of extract data
        extract_data = []
        for i in range(len(self.raw_data_list)):
            line = self.raw_data_list[i]
            #pattern = re.compile(self.extract_regexp)
            pattern =re.compile(self.basic_c)
            m = re.search(pattern, line)
            if m is not None:
                result = m.group()
                extract_data.append(result)
                exp_result.append((i, result))

        if len(extract_data):
            self.res['extract_match_flag'] = True
            self.res['extract_data_result'] = exp_result
            self.res['extract_data'] = extract_data
        else:
            self.res['extract_match_flag'] = False
            self.res['error_msg'] = constants.NO_MATCH_EXTRACT_DATA_REGEXP
        return [self.res]

    def expect_line_extract(self):
        self.__set_input__()
        line_num = len(self.raw_data_list)
        if line_num>0:
            self.res['extract_data'] = len(self.raw_data_list)
            self.res['extract_data_result'] = [(0, len(self.raw_data_list))]
            self.res['extract_match_flag'] = True
        else:
            self.res['extract_match_flag'] = False
            self.res['error_msg'] = constants.NO_EXTRACT_LINE_NUM
        return [self.res]

    def all_extract(self):
        self.__set_input__()
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
        return self.res

    @staticmethod
    def __get_space_count__(input_str):
        space_count = 0
        for s in input_str:
            if s.isspace():
                space_count += 1
            else:
                break
        return space_count

    def extract_block_by_indent(self):
        self.__set_input__()
        start_match_pattern = self.block_start_characters
        start_mark = False
        block_start_line_num = 0
        start_string = ''
        base_space_num = 0
        result = []
        line_num = self.start_line
        serial_num = 0
        identifier = ''
        for one_line in self.raw_data_list:
            start_reg_match = re.search(start_match_pattern, one_line)
            if not start_mark and start_reg_match:
                # the first match
                start_mark = True
                block_start_line_num = line_num
                start_string = start_reg_match.group()
                identifier = start_string
                base_space_num = self.__get_space_count__(one_line)
                line_num += 1
                if self.is_serial:
                    identifier = '{}_{}'.format(start_string, serial_num)
                    serial_num +=1
                continue
            if start_mark:
                cur_space_num = self.__get_space_count__(one_line)
                # if the line is block end line
                if cur_space_num <= base_space_num:
                    block_end_line_num = line_num - 1
                    # clear buffer
                    base_space_num = 0
                    start_mark = False
                    # save the block
                    res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': start_string,
                        'identifier_line_num': block_start_line_num,
                        'block_path': self.__set_block_path__(identifier),
                        'deep': self.deep
                        # 'extract_data': '\n'.join(self.data_list[block_start_line_num: block_end_line_num+1])
                    }
                    result.append(res_dict)
                    # res_dict.clear()
                    # if the line is  a new block's start line
                    if start_reg_match:
                        start_mark = True
                        block_start_line_num = line_num
                        start_string = start_reg_match.group()
                        identifier = start_string
                        if self.is_serial:
                            identifier = '{}_{}'.format(start_string, serial_num)
                            serial_num += 1
                        base_space_num = self.__get_space_count__(one_line)
            line_num += 1

        # if the last line is the last block end
        # you must save the last block info
        if start_mark:
            block_end_line_num = self.end_line
            if self.is_serial:
                identifier = start_string
            else:
                identifier = '{}_{}'.format(start_string, serial_num)
            res_dict = {
                'start_line': block_start_line_num,
                'end_line': block_end_line_num,
                'block_start_characters': start_string,
                'identifier_line_num': block_start_line_num,
                'block_path': self.__set_block_path__(identifier),
                'deep': self.deep
                # 'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num+1])
            }
            result.append(res_dict)
        return result

    def extract_block_by_line_num(self):
        self.__set_input__()
        start_match_pattern = self.block_start_characters
        block_start_line_num = 0
        start_string = ''
        result = []
        start_mark = False
        identifier = ''
        identifier_line_num = None
        serial_num = 0
        line_num = self.start_line
        for i in range(len(self.raw_data_list)):
            oneLine = self.raw_data_list[i]
            start_reg_match = re.search(start_match_pattern, oneLine)
            if start_reg_match and start_mark is False:
                start_mark = True
                block_start_line_num = line_num + self.block_start_offset
                block_end_line_num = line_num + self.block_end_offset
                # block_start_line_num and block_end_line_num is out of text range
                if block_start_line_num < 0:
                    block_start_line_num = line_num
                if block_end_line_num > self.end_line:
                    block_end_line_num = self.end_line
                start_string = start_reg_match.group()
                identifier = start_string
                identifier_line_num = line_num
                if self.is_serial:
                    identifier = '{}_{}'.format(start_string, serial_num)
                    serial_num +=1
                line_num += 1
                continue

            if start_mark:
                # the block is end
                if line_num == block_end_line_num:
                    # save the block information
                    # save the block
                    res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': start_string,
                        'identifier_line_num': identifier_line_num,
                        'block_path': self.__set_block_path__(identifier),
                        'deep': self.deep
                        # 'extract_data': '\n'.join(self.data_list[block_start_line_num: block_end_line_num+1])
                    }
                    result.append(res_dict)
                    start_mark = False
            line_num += 1
        return result

    def extract_block_by_string_range(self):
        self.__set_input__()
        start_match_pattern = self.block_start_characters
        end_match_pattern = self.block_end_characters
        identifier_match_pattern = self.extract_regexp
        block_start_line_num = 0
        block_end_line_num = 0
        start_string = ''
        end_string = ''
        identifier = ''
        identifier_line_num = None
        result = []
        start_mark = False
        serial_num = 0

        line_num = self.start_line
        for oneLine in self.raw_data_list:
            start_reg_match = re.search(start_match_pattern, oneLine)
            end_reg_match = re.search(end_match_pattern, oneLine)
            identifier_match = re.search(identifier_match_pattern, oneLine)
            # There is the case that the start string and the end string is the same reg,
            # so must check the line that is match the end string in first step
            if start_mark:
                # the block is end
                if end_reg_match:
                    if self.is_include_end_characters:
                        block_end_line_num = line_num
                    else:
                        block_end_line_num = line_num - 1
                    end_string = end_reg_match.group()
                    res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': start_string,
                        'block_end_characters': end_string,
                        'identifier_line_num': identifier_line_num,
                        'block_path': '{},{}'.format(self.block_path, identifier),
                        'is_include': self.is_include_end_characters,
                        'deep': self.deep
                        # 'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num + 1])
                    }
                    result.append(res_dict)
                    start_mark = False
                    block_start_line_num = 0
                    start_string = ''
                    end_string = ''

            if start_reg_match and start_mark is False:
                # the block is start
                start_mark = True
                block_start_line_num = line_num
                start_string = start_reg_match.group()
                if identifier_match:
                    identifier = identifier_match.group()
                    identifier_line_num = line_num
                    if self.is_serial:
                        identifier = '{}_{}'.format(identifier, serial_num)
                        serial_num +=1


            line_num += 1
        # there is the case that  the last line is the text end and  the start string had been matched
        # in the case you must save the last block info
        if start_mark:
            block_end_line_num = self.end_line
            res_dict = {
                'start_line': block_start_line_num,
                'end_line': block_end_line_num,
                'block_start_characters': start_string,
                'block_end_characters': end_string,
                'identifier_line_num': identifier_line_num,
                'block_path': self.__set_block_path__(identifier),
                'is_include': self.is_include_end_characters,
                'deep': self.deep
                # 'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num + 1])
            }
            result.append(res_dict)
        return result

    def extract_block_by_regular(self):
        self.__set_input__()
        basic_pattern = self.basic_c
        block_start_line_num = 0
        lineNum_list = []
        line_count = 0
        block_start_mark = False
        result = []
        for one_line in self.raw_data_list:
            basic_pattern_match = re.search(basic_pattern, one_line)
            if basic_pattern_match:
                match_string = basic_pattern_match.group()
                line_num = self.start_line + line_count
                lineNum_list.append((line_num, match_string))
                if not block_start_mark:
                    block_start_line_num = self.start_line + line_count
                block_start_mark = True
            else:
                if block_start_mark:
                    block_end_line_num = self.start_line + line_count - 1
                    res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': self.basic_c,
                        'deep': self.deep,
                        'block_path': self.__set_block_path__(self.basic_c),
                        'reg_match_context': lineNum_list
                        # 'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num + 1])
                    }
                    result.append(res_dict)
                    # clear buffer
                    block_start_mark = False
                    lineNum_list = []
                    block_start_line_num = 0
            line_count += 1
        if block_start_mark:
            # block_end_line_num = self.end_line
            res_dict = {
                'start_line': block_start_line_num,
                'end_line': self.end_line,
                'block_start_characters': self.basic_c,
                'block_path':  self.__set_block_path__(self.basic_c),
                'deep': self.deep,
                'reg_match_context': lineNum_list
                # 'extract_data': '\n'.join(self.data_list[block_start_line_num:])
            }
            result.append(res_dict)

        return result

