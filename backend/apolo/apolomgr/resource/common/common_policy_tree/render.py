#!/usr/bin/env python


'''

@author: kimli
@contact: kimli@cisco.com
@file: render.py
@time: 2017/12/18
@desc:

'''

# import os, sys

from backend.apolo.apolomgr.resource.common.common_policy_tree.dispatch import Dispatch
from backend.apolo.apolomgr.resource.common.common_policy_tree.tool import Tool
from backend.apolo.db_utils.db_opt import DBOpt
from backend.apolo.models import CollPolicyCliRule


class Render(Tool, DBOpt):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.data = kwargs['data']
        self.tree= kwargs['tree']  # json data from front
        self.tree_id = kwargs['tree_id'] # the clicked tree node id
        # save format [leaf rule_id,parent rule_id...root rule_id]
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
            print buffer_dict["children"]
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
            rule_context =self.__get_rule_from_db__(rule_id)
            # save the data as input of rules
            if not self.rule_context.has_key(rule_id):
                self.rule_context.update({rule_id: rule_context})
        arry =self.leaf_path
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
        deep = len(self.leaf_path)-1
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
                        if i == start_line:
                            all_data[i] = '<div style="background-color:{};display: inline-block;">{}'.format(
                                self.colors[deep][color_index], all_data[i])
                            color_index += 1
                        if i == end_line:
                            all_data[i] = all_data[i] + '</div>'
            deep = deep - 1
        html_data = "\n".join(all_data)
        return html_data


    def __get_rule_from_db__(self, rule_id):
       obj = self.get_rule_detail_from_db(rule_id)
       return self.get_rule_value(obj)

if __name__ == '__main__':
    queryset = CollPolicyCliRule.objects.filter(coll_policy=1)
    r = Render(**{"data":"","tree":"","tree_id":""})
    for recoder in queryset:
        k = r.get_rule_value(recoder)
        print k








