#!/usr/bin/env python


'''

@author: kimli
@contact: kimli@cisco.com
@file: render.py
@time: 2017/12/18
@desc:

'''
import sys
import os

script_dir = os.path.split(os.path.realpath(__file__))[0]
prj_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.append(prj_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

import django
django.setup()

from backend.apolo.models import CollPolicyCliRule
from dispatch import Dispatch

class Render(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.data = kwargs['data']
        self.tree= kwargs['tree']
        self.tree_id = kwargs['tree_id'] #the clicked tree node id
        # save format [(leaf tree_id,leaf rule_id),(parent tree_id,parent rule_id)...(root tree_id,root rule_id)]
        self.leaf_path = []
        self.rule_context = {}

        self.dispatch_result = {}
        self.colors = [
                        ["#FDEDEC", "#EBF5FB", "#F5EEF8", "#FEF9E7", "#F8F9F9"],
                        ["#FADBD8", "#D6EAF8", "#EBDEF0", "#FCF3CF", "#F2F3F4"],
                        ["#F5B7B1", "#AED6F1", "#D7BDE2", "#F9E79F", "#E5E7E9"]
                      ]

    def render(self):

        # get leaf path
        self.get_path_of_leaf(self.tree)
        self.execute_dispatch()

        html_text = self.generate_html()
        return html_text

    # get the path that is from root to the leaf node
    def get_path_of_leaf(self, buffer_dict):

        if buffer_dict['id'] == self.tree_id:
            # save the leaf node
            self.leaf_path.append((buffer_dict['id'], buffer_dict['rule_id']))
            return True

        if buffer_dict["children"]:
            for d in buffer_dict["children"]:
                if self.get_path_of_leaf(d):
                    # save the parent node of the leaf
                    # if buffer_dict['rule_id'] != 0:
                    if buffer_dict['rule_id']:
                        self.leaf_path.append((buffer_dict['id'], buffer_dict['rule_id']))
                    return True

    # get the dispatch executed result
    def execute_dispatch(self):

        for i in self.leaf_path:
            tree_id = i[0]
            rule_id = i[1]
            rule_context =self.__get_rule_from_db__(rule_id)
            # save the data as input of rules
            self.rule_context.update({tree_id: rule_context})
        arry =self.leaf_path
        arry.reverse()
        the_first_data = self.rule_context[arry[0][0]]
        # set the init data
        the_first_data['data'] = self.data
        the_first_data['start_line'] = 0
        the_first_data['end_line'] = len(self.data.split('\n'))-1
        p = Dispatch(arry, self.rule_context, the_first_data)
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
        while deep >= 0:
            color_index = 0
            # leaf node area
            node = self.dispatch_result[deep]
            for item in node:
                # mark the extracted data
                # get the returned value
                # the node is leaf
                if item.has_key('isleaf'):
                    basic_character_index = item['basic_character_index']
                    extract_data_index = item['extract_data_index']
                    start_line = item['start_line']
                    end_line = item['end_line']
                    # split raw data
                    data_list = all_data[start_line:end_line + 1]
                    context = '\n'.join(data_list)
                    context_list = context.split(' ')
                    # replace string
                    basic_character = context_list[basic_character_index]
                    extract_data = context_list[extract_data_index]
                    # add color for extracted data
                    context_list[basic_character_index] = '<font color="red">{}</font>'.format(basic_character)
                    context_list[extract_data_index] = '<font color="green">{}</font>'.format(extract_data)
                    html_context = ' '.join(context_list)
                    # replace block
                    html_context_list = html_context.split('\n')
                    j = 0
                    for i in range(len(all_data)):
                        if i == start_line and i < end_line + 1:
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
                        if i == start_line:
                            all_data[i] = '<div style="background-color:{};display: inline-block;">{}'.format(
                                self.colors[deep][color_index], all_data[i])
                            color_index += 1
                        if i == end_line:
                            all_data[i] = all_data[i] + '</div>'
            deep = deep - 1
        html_data = '<pre>{}</pre>'.format("\n".join(all_data))
        return html_data

    @staticmethod
    def __get_rule_from_db__(rule_id):
        obj = CollPolicyCliRule.objects.get(ruleid=rule_id)
        # set input
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



