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
        self.data = """w34nh-----imnt000100#show interfaces
Load for five secs: 3%/0%; one minute: 1%; five minutes: 1%
Time source is NTP, 12:29:03.494 JST Wed Oct 11 2017

GigabitEthernet0/0/0 is up, line protocol is up
  Hardware is 4XGE-BUILT-IN, address is 2c54.2d61.7200 (bia 2c54.2d61.7200)
  Internet address is 10.92.51.106/30
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported
  Full Duplex, 10008, link type is force-up, media type is T
  output flow-control is on, input flow-control is on
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 02:45:36, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: Class-based queueing
  Output queue: 0/40 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     901097 packets input, 70495509 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 638231 multicast, 0 pause input
     280805 packets output, 26218227 bytes, 0 underruns
     0 output errors, 0 collisions, 2 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out
GigabitEthernet0/0/1 is up, line protocol is up
  Hardware is 4XGE-BUILT-IN, address is 2c54.2d61.7201 (bia 2c54.2d61.7201)
  Internet address is 10.92.51.234/30
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported
  Full Duplex, 10009, link type is auto, media type is T
  output flow-control is on, input flow-control is on
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 01:50:16, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: Class-based queueing
  Output queue: 0/40 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     740674 packets input, 59583182 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 638387 multicast, 0 pause input
     110833 packets output, 14928926 bytes, 0 underruns
     0 output errors, 0 collisions, 2 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out"""""
        # get leaf path
        self.get_path_of_leaf(self.tree)
        self.execute_dispatch()

        html_text = self.generate_html()
        return html_text

    # get the path that is from root to the clicked node
    # save format :[rule_id1,rule_id2...rule_idn]
    def get_path_of_leaf(self, buffer_dict):

        if buffer_dict['id'] == self.tree_id:
            # save the leaf node
            self.leaf_path.append(buffer_dict['rule_id'])
            return True

        if buffer_dict["children"]:
            for d in buffer_dict["children"]:
                if self.get_path_of_leaf(d):
                    # save the parent node of the leaf
                    # if buffer_dict['rule_id'] != 0:
                    if buffer_dict['rule_id']:
                        self.leaf_path.append(buffer_dict['rule_id'])
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


    def __get_rule_from_db__(self, rule_id):
       obj = self.get_rule_detail_from_db(rule_id)
       return self.get_rule_value(obj)

if __name__ == '__main__':
    queryset = CollPolicyCliRule.objects.filter(coll_policy=1)
    r = Render(**{"data":"","tree":"","tree_id":""})
    for recoder in queryset:
        k = r.get_rule_value(recoder)
        print k








