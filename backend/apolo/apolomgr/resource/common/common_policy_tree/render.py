#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''

@author: Gin Chen
@contact: Gin Cheni@cisco.com
@file: render.py
@time: 2017/12/18
@desc:

'''

# import os, sys
import re

from backend.apolo.apolomgr.resource.common.common_policy_tree.dispatch import Dispatch
from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.db_utils.db_opt import DBOpt
from backend.apolo.tools import constants


class Render(Tool, DBOpt):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.data = kwargs['data']
        self.tree = kwargs['tree']  # json data from front
        self.tree_id = kwargs['tree_id']  # the clicked tree node id
        # save format [leaf rule_id,parent rule_id...root rule_id]
        self.leaf_path = []
        self.rule_context = {}
        self.dispatch_result = {}

    def render(self):
        """!@brief
        main process of highlight function
        @param
        @pre :Post function of PolicyTreeHighLightViewSet
        @post
        @note
        @return rule info
        @author Gin Chen
        @date 2017/12/18
        """
        # get leaf path
        self.get_path_of_leaf(self.tree)
        # do work follow
        self.execute_dispatch()
        # render by result of dispatch
        if self.dispatch_result:
            html_text = self.generate_html()
        else:
            html_text = None
        return html_text

    def get_path_of_leaf(self, tree_dict):
        """!@brief
        get the path that is from root to the clicked node
        @param tree_dict: tree data from request
        @pre :Post function of PolicyTreeHighLightViewSet
        @post
        @note  save format :[rule_id1,rule_id2...rule_idn]
        @return path of leaf
        @author Gin Chen
        @date 2017/12/18
        """

        if tree_dict['id'] == self.tree_id:
            # save the leaf node
            self.leaf_path.append(tree_dict['data']['rule_id'])
            return True

        if tree_dict["children"]:
            for d in tree_dict["children"]:
                if self.get_path_of_leaf(d):
                    # save the parent node of the leaf
                    if tree_dict['data']['rule_id']:
                        self.leaf_path.append(tree_dict['data']['rule_id'])
                    return True


    def execute_dispatch(self):
        """!@brief
       # get the dispatch executed result
       @param
       @pre :render.py.render
       @post
       @note  self.dispatch_result format: {deep:[{startline, endline..},{}]}
       @return self.dispatch_result
       @author Gin Chen
       @date 2017/12/18
       """
        for rule_id in self.leaf_path:
            rule_context = self.__get_rule_from_db(rule_id)
            # save the data as input of rules
            if not self.rule_context.has_key(rule_id):
                self.rule_context.update({rule_id: rule_context})
        arry = self.leaf_path
        arry.reverse()
        p = Dispatch(arry, self.rule_context, self.data)
        p.dispatch()
        arry = p.get_result()

        for parent_item in arry:
            for child_item in parent_item:
                deep = child_item['deep']
                if self.dispatch_result.has_key(deep):
                    self.dispatch_result[deep].append(child_item)
                else:
                    self.dispatch_result[deep] = [child_item]


    def generate_html(self):
        """!@brief
        generate highlight data html page
        @param
        @pre : get highlight info by rule. function:render.py.render
        @post
        @note
        @return highlight html
        @author Gin Chen
        @date 2017/12/18
        """
        # render
        deep = len(self.leaf_path) - 1
        # chance xml mark
        self.data = Tool.replace_xml_mark(self.data)
        all_data = self.data.split('\n')
        # start_line = 0
        # end_line = len(all_data)
        while deep >= 0:
            color_index = 0
            # leaf node area
            node = self.dispatch_result[deep]
            for item in node:
                # mark the extracted data
                # get the returned value
                # the node is leaf
                if item.has_key('isleaf'):
                    if not item['extract_match_flag']:
                        pass
                    else:
                        basic_character_index = item['basic_character_index']
                        basic_character = Tool.replace_xml_mark(item['basic_character'])
                        extract_data_pair = item['extract_data_result']
                        start_line = item['start_line']
                        end_line = item['end_line']
                        split_char_reg = item['split_characters']
                        split_char = self.__get_split_char(split_char_reg)
                        rule_type = item['rule_type']
                        # get block text
                        data_list = all_data[start_line:end_line + 1]
                        if rule_type == 3:
                            for pair in extract_data_pair:
                                extract_data = pair[1]
                                line_index = pair[0]
                                replace_extract_data = '{}{}{}'.format(constants.EXTRACT_DATA_STYLE,
                                                                       extract_data,
                                                                       constants.SPAN_END)
                                data_list[line_index] = data_list[line_index].replace(
                                    extract_data, replace_extract_data)
                            html_context = '\n'.join(data_list)
                        elif rule_type == 4:
                            # show line num
                            # there is one layer
                            if deep == 0:
                                extract_data = extract_data_pair[0][1]
                                show_line_num = constants.EXTRACT_LINE_NUM_STYLE.format(extract_data)
                                all_data[0] = str(show_line_num) + constants.LINE_NUM_MSG_REPLACE + str(all_data[0])
                                continue
                            # there is two layers
                            elif deep == 1:
                                before_node = self.dispatch_result[0][0]
                                if before_node['rule_type'] == 8:
                                    extract_data = extract_data_pair[0][1]
                                    show_line_num = constants.EXTRACT_LINE_NUM_STYLE.format(extract_data)
                                    all_data[0] = str(show_line_num) + constants.LINE_NUM_MSG_REPLACE + str(all_data[0])
                                    continue
                                else:
                                    html_context = '\n'.join(data_list)
                                    extract_data = extract_data_pair[0][1]
                                    show_line_num = constants.EXTRACT_LINE_NUM_STYLE.format(extract_data)
                                    html_context = str(show_line_num) + constants.LINE_NUM_MSG_REPLACE + str(
                                        html_context)
                            elif deep == 2:
                                top_node = self.dispatch_result[0][0]
                                before_node = self.dispatch_result[1][0]
                                if before_node['rule_type'] == 8:
                                    extract_data = extract_data_pair[0][1]
                                    show_line_num = constants.EXTRACT_LINE_NUM_STYLE.format(extract_data)
                                    ln = top_node['start_line']
                                    all_data[ln] = str(show_line_num) + constants.LINE_NUM_MSG_REPLACE + str(
                                        all_data[ln])
                                    continue
                                else:
                                    html_context = '\n'.join(data_list)
                                    extract_data = extract_data_pair[0][1]
                                    show_line_num = constants.EXTRACT_LINE_NUM_STYLE.format(extract_data)
                                    html_context = str(show_line_num) + constants.LINE_NUM_MSG_REPLACE + str(
                                        html_context)
                            else:
                                continue

                        elif rule_type == 9:
                            for i in range(len(data_list)):
                                data_list[i] = '{}{}{}'.format(constants.EXTRACT_DATA_STYLE, data_list[i],
                                                               constants.SPAN_END)
                            html_context = '\n'.join(data_list)
                        else:
                            extract_data_index = extract_data_pair[0][0]
                            extract_data = Tool.replace_xml_mark(extract_data_pair[0][1])
                            # replace basic character with split char in raw data
                            replace_char = basic_character
                            if split_char in basic_character:
                                replace_char = basic_character.replace(split_char, constants.INSTEAD)

                            basic_character_line_num = item['basic_character_line_num']
                            # if there are many basic_characters in the line,replace the first basic_character
                            data_list[basic_character_line_num] = data_list[basic_character_line_num]. \
                                replace(basic_character, '{}{}{}'.format(constants.REPLACE_START_MARK,
                                                                         replace_char, constants.REPLACE_END_MARK),
                                        1)

                            # combine to new text
                            element_index = 0
                            is_chanced = 0
                            for i in range(len(data_list)):
                                line = data_list[i]
                                line_arry = re.split(split_char_reg, line)
                                for j in range(len(line_arry)):
                                    if element_index == basic_character_index:
                                        basic_character_new = line_arry[j]
                                        if constants.INSTEAD in basic_character_new:
                                            basic_character_new = basic_character_new.replace(constants.INSTEAD,
                                                                                              split_char)
                                        # the basic char is same with extracted data
                                        if basic_character_index == extract_data_index:
                                            basic_character_new = basic_character_new.replace(
                                                constants.REPLACE_START_MARK,
                                                constants.EXTRACT_DATA_STYLE
                                            )
                                            basic_character_new = basic_character_new.replace(
                                                constants.REPLACE_END_MARK,
                                                constants.SPAN_END
                                            )
                                        else:
                                            basic_character_new = basic_character_new.replace(
                                                constants.REPLACE_START_MARK,
                                                constants.BASIC_CHAR_STYLE
                                            )
                                            basic_character_new = basic_character_new.replace(
                                                constants.REPLACE_END_MARK,
                                                constants.SPAN_END
                                            )
                                        line_arry[j] = basic_character_new
                                        is_chanced += 1
                                    elif element_index == extract_data_index:
                                        replace_extract_data = '{}{}{}'.format(constants.EXTRACT_DATA_STYLE,
                                                                               extract_data,
                                                                               constants.SPAN_END)
                                        line_arry[j] = line_arry[j].replace(extract_data, replace_extract_data)
                                        is_chanced += 1
                                    else:
                                        pass
                                    if is_chanced > 0:
                                        data_list[i] = data_list[i].replace(data_list[i],
                                                                            split_char.join(line_arry))
                                    if is_chanced == 2:
                                        break
                                    element_index += 1
                            html_context = '\n'.join(data_list)
                            # replace block
                        html_context_list = html_context.split('\n')
                        j = 0
                        for i in range(len(all_data)):
                            if start_line <= i:
                                if i < end_line + 1:
                                    all_data[i] = html_context_list[j]
                                    j = j + 1
                else:
                    # the node is not leaf
                    # the node is block area
                    start_line = item['start_line']
                    end_line = item['end_line']
                    basic_char_line = item['block_basic_line_num']
                    # mark the block basic char
                    block_start_char = Tool.replace_xml_mark(item['block_start_characters'])
                    extract_data_in_block_basic = False
                    if constants.EXTRACT_DATA_STYLE in all_data[basic_char_line]:
                        extract_match = re.search(
                            '{}(.*){}'.format(constants.EXTRACT_DATA_STYLE,
                                              constants.SPAN_END),
                            all_data[basic_char_line])
                        if extract_match is not None:
                            buffer_data = extract_match.group(1)
                            if buffer_data in block_start_char \
                                    or block_start_char in buffer_data:
                                extract_data_in_block_basic = True

                    if not extract_data_in_block_basic:
                        all_data[basic_char_line] = all_data[basic_char_line].replace(block_start_char,
                                                                                      '{}{}{}'.format(
                                                                                          constants.BLOCK_BASIC_CHAR_STYLE,
                                                                                          block_start_char,
                                                                                          constants.SPAN_END))

                    # add block start html mark for a block
                    block_rule_style = constants.BLOCK_RULE_EVEN_STYLE
                    if color_index == 1:
                        block_rule_style = constants.BLOCK_RULE_ODD_STYLE

                    if item['rule_type'] != 8:
                        all_data[start_line] = '{}{}'.format(block_rule_style, all_data[start_line])
                        if color_index == 1:
                            color_index = 0
                        else:
                            color_index = 1

                    # if  block rule is block_rule_by_regular
                    if item.has_key('reg_match_context'):
                        for tuple_item in item['reg_match_context']:

                            (lm, match_string) = tuple_item
                            match_string = Tool.replace_xml_mark(match_string)
                            if constants.EXTRACT_DATA_STYLE in all_data[lm]:
                                extract_match = re.search(
                                    '{}(.*){}'.format(constants.EXTRACT_DATA_STYLE, constants.SPAN_END),
                                    all_data[lm])
                                if extract_match is not None:
                                    buffer_data = extract_match.group(1)
                                    if buffer_data in match_string or match_string in buffer_data:
                                        all_data[lm] = constants.REGEXP_BLOCK_RULE_STYLE.format(all_data[lm])
                                        continue

                            all_data[lm] = all_data[lm].replace(match_string,
                                                                '{}{}{}'.format(
                                                                    constants.BLOCK_BASIC_CHAR_STYLE,
                                                                    match_string,
                                                                    constants.SPAN_END))
                            all_data[lm] = constants.REGEXP_BLOCK_RULE_STYLE.format(all_data[lm])

                    # add block end html mark for a block
                    if item['rule_type'] != 8:
                        if item.has_key('is_include'):
                            if not item['is_include']:
                                block_end_char = Tool.replace_xml_mark(item['block_end_characters'])
                                is_marked = False
                                if constants.EXTRACT_DATA_STYLE in all_data[end_line]:
                                    extract_match = re.search(
                                        '{}(.*){}'.format(constants.EXTRACT_DATA_STYLE,
                                                          constants.SPAN_END),
                                        all_data[end_line])
                                    if extract_match is not None:
                                        buffer_data = extract_match.group(1)
                                        if buffer_data in block_end_char \
                                                or block_end_char in buffer_data:
                                            is_marked = True
                                if not is_marked:
                                    all_data[end_line] = all_data[end_line].replace(block_end_char,
                                                                                    '{}{}{}'.format(
                                                                                        constants.BLOCK_BASIC_CHAR_STYLE,
                                                                                        block_end_char,
                                                                                        constants.SPAN_END))

                        if all_data[end_line]:
                            all_data[end_line] = all_data[end_line] + constants.DIV_END
                        else:
                            # there is only enter key in the end line
                            all_data[end_line] = all_data[end_line] + ' ' + constants.DIV_END
            deep = deep - 1
        html_data_list = []
        for k in range(len(all_data)):
            arry = []
            if constants.LINE_NUM_MSG_REPLACE in all_data[k]:
                arry = all_data[k].replace(constants.LINE_NUM_MSG_REPLACE, '\n')
            if len(arry) > 0:
                html_data_list.append(arry)
            else:
                html_data_list.append(all_data[k])
        html_data = "\n".join(html_data_list)
        return html_data

    def __get_rule_from_db(self, rule_id):
        """!@brief
        get rule info from db
        @param rule_id:rule id
        @pre : function:render.py.execute_dispatch
        @post
        @note
        @return rule info
        @author Gin Chen
        @date 2017/12/18
        """
        obj = self.get_rule_detail_from_db(rule_id)
        return self.get_rule_value(obj)

    def __get_split_char(self, split_char_reg):
        """!@brief
        get split char by split char regex
        @param split_char_reg: regex of split char
        @pre
        @post
        @note
        @return split char
        @author Gin Chen
        @date 2017/12/18
        """
        if split_char_reg:
            m = re.search(split_char_reg, self.data)
            if m is not None:
                return m.group()
            else:
                return split_char_reg
        else:
            return split_char_reg
