#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''

@author: kimli
@contact: kimli@cisco.com
@file: render.py
@time: 2017/12/18
@desc:

'''

# import os, sys
import re

from backend.apolo.apolomgr.resource.common.common_policy_tree.dispatch import Dispatch
from backend.apolo.apolomgr.resource.common.common_policy_tree.tool import Tool
from backend.apolo.db_utils.db_opt import DBOpt
from backend.apolo.models import CollPolicyCliRule
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
        self.colors = [
            ["rgba(245, 180, 145, 0.15)", "rgba(250, 155, 190, 0.15)"],
            ["rgba(245, 180, 145, 0.15)", "rgba(250, 155, 190, 0.15)"],
            ["#F5B7B1", "#AED6F1", "#D7BDE2", "#F9E79F", "#E5E7E9"]
        ]

    def render(self):
        # get leaf path
        self.get_path_of_leaf(self.tree)
        self.execute_dispatch()
        if self.dispatch_result:
            html_text = self.generate_html()
        else:
            html_text = None
        return html_text

    # get the path that is from root to the clicked node
    # save format :[rule_id1,rule_id2...rule_idn]
    def get_path_of_leaf(self, buffer_dict):

        if buffer_dict['id'] == self.tree_id:
            # save the leaf node
            self.leaf_path.append(buffer_dict['data']['rule_id'])
            return True

        if buffer_dict["children"]:
            for d in buffer_dict["children"]:
                if self.get_path_of_leaf(d):
                    # save the parent node of the leaf
                    # if buffer_dict['rule_id'] != 0:
                    if buffer_dict['data']['rule_id']:
                        self.leaf_path.append(buffer_dict['data']['rule_id'])
                    return True

    # get the dispatch executed result
    def execute_dispatch(self):
        for rule_id in self.leaf_path:
            rule_context = self.__get_rule_from_db__(rule_id)
            # save the data as input of rules
            if not self.rule_context.has_key(rule_id):
                self.rule_context.update({rule_id: rule_context})
        arry = self.leaf_path
        arry.reverse()
        p = Dispatch(arry, self.rule_context, self.data)
        p.dispatch()
        arry = p.get_result()
        # save format as like {deep:[{startline, endline..},{}]}
        for parent_item in arry:
            for child_item in parent_item:
                deep = child_item['deep']
                if self.dispatch_result.has_key(deep):
                    self.dispatch_result[deep].append(child_item)
                else:
                    self.dispatch_result[deep] = [child_item]

    def generate_html(self):
        # render
        deep = len(self.leaf_path) - 1
        all_data = self.data.split('\n')
        start_line = 0
        end_line = len(all_data)
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
                        # command xml tag
                        basic_character_index = item['basic_character_index']
                        basic_character = item['basic_character']
                        extract_data_pair = item['extract_data_result']
                        start_line = item['start_line']
                        end_line = item['end_line']
                        split_char = item['split_characters']
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
                            data_list[0] = '{}{}'.format(constants.EXTRACT_DATA_STYLE, data_list[0])
                            data_list[-1] = '{}{}'.format(data_list[-1], constants.SPAN_END)
                            html_context = '\n'.join(data_list)
                        else:
                            extract_data_index = extract_data_pair[0][0]
                            extract_data = extract_data_pair[0][1]
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
                            # there is Regular expression special chars in split char
                            sp_char = Tool.replace_escape_char(split_char)
                            for i in range(len(data_list)):
                                line = data_list[i]
                                line_arry = re.split(sp_char, line)
                                # line_arry = re.split(split_char, line)
                                for j in range(len(line_arry)):
                                    if element_index == basic_character_index:
                                        basic_character_new = line_arry[j]
                                        if constants.INSTEAD in basic_character_new:
                                            basic_character_new = basic_character_new.replace(constants.INSTEAD,
                                                                                              split_char)
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
                    # node = self.dispatch_result[deep]
                    # for item in node:
                    start_line = item['start_line']
                    end_line = item['end_line']
                    for i in range(len(all_data)):
                        if item.has_key('identifier_line_num'):
                            if i == item['identifier_line_num']:
                                if constants.EXTRACT_DATA_STYLE in all_data[i]:
                                    extract_match = re.search(
                                        '{}(.*){}'.format(constants.EXTRACT_DATA_STYLE,
                                                          constants.SPAN_END),
                                        all_data[i])
                                    if extract_match is not None:
                                        buffer_data = extract_match.group(1)
                                        if buffer_data in item['block_start_characters'] \
                                                or item['block_start_characters'] in buffer_data:
                                            continue

                                all_data[i] = all_data[i].replace(item['block_start_characters'],
                                                              '{}{}{}'.format(constants.BLOCK_BASIC_CHAR_STYLE,
                                                                              item['block_start_characters'],
                                                                              constants.SPAN_END))

                        if i == start_line:
                            block_rule_style = constants.BLOCK_RULE_EVEN_STYLE
                            if color_index==1:
                                block_rule_style = constants.BLOCK_RULE_ODD_STYLE

                            if item['rule_type'] != 8:
                                all_data[i] = '{}{}'.format(block_rule_style, all_data[i])

                                if color_index == 1:
                                    color_index = 0
                                else:
                                    color_index = 1
                            # if  block rule is block_rule_by_regular
                            if item.has_key('reg_match_context'):
                                for tuple_item in item['reg_match_context']:

                                    (lm, match_string) = tuple_item
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


                        if i == end_line and item['rule_type'] != 8:
                            if item.has_key('is_include'):
                                if item['is_include']:
                                    all_data[i] = all_data[i].replace(item['block_end_characters'],
                                                                      '{}{}{}'.format(
                                                                          constants.BLOCK_BASIC_CHAR_STYLE,
                                                                          item['block_end_characters'],
                                                                          constants.SPAN_END))

                            if all_data[i]:
                                all_data[i] = all_data[i] + constants.DIV_END
                            else:
                                # there is only enter key in the end line
                                all_data[i] = all_data[i] + ' ' + constants.DIV_END
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

    def __get_rule_from_db__(self, rule_id):
        obj = self.get_rule_detail_from_db(rule_id)
        return self.get_rule_value(obj)
