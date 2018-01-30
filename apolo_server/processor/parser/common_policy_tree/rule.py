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


    def __split_data__(self):

        if self.deep > 0:
            self.start_line +=1
        self.data_list = self.data.split('\n')[self.start_line:self.end_line + 1]

    def __set_input__(self):

        # self.data = self.extract_policy['data']
        self.start_line = self.extract_policy['start_line']
        self.end_line = self.extract_policy['end_line']
        self.x_offset = self.extract_policy['x_offset']
        self.y_offset = self.extract_policy['y_offset']
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
        self.raw_data_list = self.data.split('\n')[self.start_line:self.end_line + 1]
        self.instead = constants.INSTEAD
        self.render_b_c = ''
        # data extraction's result
        self.res = {
            'start_line': self.start_line,  # the starting position of a line
            'end_line': self.end_line,  # the ending position of a line
            'block_start_characters': self.block_start_characters,  # the starting character of block
            'block_end_characters': self.block_end_characters,  # the ending character of block
            'basic_character_index': None,  # the basic character position
            'basic_character': None,  # the basic character
            'extract_data_index': None,  # the extract data position
            'extract_data': None, # the extract data
            'deep':self.deep,
            'isleaf':True
        }
        self.data_list = []
        self.__split_data__()

    def x_offset_space_extract(self):

        self.__set_input__()
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
        return [self.res]

    def x_offset_comma_extract(self):
        self.__set_input__()
        pass

    def x_offset_slash_extract(self):
        self.__set_input__()
        pass

    def y_offset_space_extract(self):
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
        self.__set_input__()
        pass

    def y_offset_slash_extract(self):
        self.__set_input__()
        pass

    def regexp_extract(self):
        self.__set_input__()
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
        self.__set_input__()
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
        print new_list[0]
        print new_list[209]
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
        start_match_pattern = "\s*(" + self.block_start_characters + ").*"
        start_mark = False
        block_start_line_num = 0
        start_string = ''
        base_space_num = 0
        result = []
        line_num = self.start_line
        for one_line in self.data_list:

            start_reg_match = re.match(start_match_pattern, one_line)
            if not start_mark and start_reg_match:
                # the first match
                start_mark = True
                block_start_line_num = line_num
                start_string = start_reg_match.group(1)
                base_space_num = self.__get_space_count__(one_line)
                line_num += 1
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
                            'deep': self.deep
                            #'extract_data': '\n'.join(self.data_list[block_start_line_num: block_end_line_num+1])
                    }

                    result.append(res_dict)
                    #res_dict.clear()
                    # if the line is  a new block's start line
                    if start_reg_match:
                        start_mark = True
                        block_start_line_num = line_num
                        start_string = start_reg_match.group(1)
                        base_space_num = self.__get_space_count__(one_line)
            line_num += 1

        # if the last line is the last block end
        # you must save the last block info
        if start_mark:
            block_end_line_num = self.end_line
            res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': start_string,
                        'deep': self.deep
                        #'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num+1])
            }
            result.append(res_dict)
        return result


    def extract_block_by_line_num(self):
        self.__set_input__()

        start_match_pattern = "\s*(" + self.block_start_characters + ").*"
        block_start_line_num = 0
        start_string = ''
        result = []
        start_mark = False
        
        line_num = self.start_line
        for oneLine in self.data_list:
            start_reg_match = re.match(start_match_pattern, oneLine)
            if start_reg_match and start_mark is False:
                start_mark = True
                block_start_line_num = line_num + self.block_start_offset
                block_end_line_num = line_num + self.block_end_offset
                # block_start_line_num and block_end_line_num is out of text range
                if block_start_line_num < 0 or block_end_line_num > self.end_line:
                    errMsg = "block is out of text range"
                    return errMsg
                start_string = start_reg_match.group(1)
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
                        'deep': self.deep
                        # 'extract_data': '\n'.join(self.data_list[block_start_line_num: block_end_line_num+1])
                    }
                    result.append(res_dict)
                    start_mark = False
            line_num += 1
        return result

    def extract_block_by_string_range(self):
        self.__set_input__()
        start_match_pattern = "\s*(" + self.block_start_characters + ").*"
        end_match_pattern = ".*(" + self.block_end_characters + ").*"
        block_start_line_num = 0
        block_end_line_num = 0
        start_string = ''
        end_string = ''
        result = []
        start_mark = False
        
        line_num = self.start_line
        for oneLine in self.data_list:
            start_reg_match = re.match(start_match_pattern, oneLine)
            end_reg_match = re.match(end_match_pattern, oneLine)
            # There is the case that the start string and the end string is the same reg,
            # so must check the line that is match the end string in first step
            if start_mark:
                # the block is end
                if end_reg_match:
                    if self.is_include_end_characters:
                        block_end_line_num = line_num
                    else:
                        block_end_line_num = line_num - 1
                    end_string = end_reg_match.group(1)
                    res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': start_string,
                        'block_end_characters': end_string,
                        'deep': self.deep
                        #'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num + 1])
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
                start_string = start_reg_match.group(1)

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
                'deep': self.deep
                #'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num + 1])
            }
            result.append(res_dict)
        return result

    def extract_block_by_regular(self):
        self.__set_input__()
        basic_pattern = '.*({}).*'.format(self.basic_c)
        block_start_line_num = 0
        lineNum_list = []
        line_count = 0
        block_start_mark = False
        result = []
        for one_line in self.data_list:
            basic_pattern_match = re.match(basic_pattern, one_line)
            if basic_pattern_match:
                match_string = basic_pattern_match.group(1)
                line_num = self.start_line + line_count
                lineNum_list.append((line_num, match_string))
                block_start_mark = True
                if block_start_line_num == 0:
                    block_start_line_num = self.start_line + line_count
            else:
                if block_start_mark:
                    block_end_line_num = self.start_line + line_count-1
                    res_dict = {
                        'start_line': block_start_line_num,
                        'end_line': block_end_line_num,
                        'block_start_characters': self.basic_c,
                        'deep': self.deep,
                        'reg_match_context': lineNum_list
                        #'extract_data': '\n'.join(self.data_list[block_start_line_num:block_end_line_num + 1])
                    }
                    result.append(res_dict)
                    # clear buffer
                    block_start_mark = False
                    lineNum_list = []
                    block_start_line_num = 0
            line_count += 1
        if block_start_mark:
            #block_end_line_num = self.end_line
            res_dict = {
                'start_line': block_start_line_num,
                'end_line': self.end_line,
                'block_start_characters': self.basic_c,
                'deep': self.deep,
                'reg_match_context': lineNum_list
                #'extract_data': '\n'.join(self.data_list[block_start_line_num:])
            }
            result.append(res_dict)

        return result

