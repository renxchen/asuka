#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: policy_tree_highlight_view.py
@time: 2017/12/18 18:24
@desc:

'''
from rest_framework import viewsets
import json

from backend.apolo.apolomgr.resource.render import Render
from backend.apolo.tools import views_helper
from backend.apolo.tools.common import api_return

class PolicyTreeHighLightViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(PolicyTreeHighLightViewSet, self).__init__(**kwargs)
        self.request = request
        self.raw_data = views_helper.get_request_body(self.request, 'raw_data')
        self.tree_id = views_helper.get_request_body(self.request, 'tree_id')
        self.tree = views_helper.get_request_body(self.request, 'tree')

    def post(self):

        # self.raw_data =views_helper.get_request_body(self.request, 'raw_data')
        # self.tree_id = views_helper.get_request_body(self.request, 'tree_id')
        # self.tree = views_helper.get_request_body(self.request, 'tree')
        self.raw_data = """w34nh-----imnt000100#show interfaces
                            Load for five secs: 3%/0%; one minute: 1%; five minutes: 1%
                            Time source is NTP, 12:29:03.494 JST Wed Oct 11 2017

                            GigabitEthernet0/0/0 is up, line protocol is up
                              Hardware is 4XGE-BUILT-IN, address is 2c54.2d61.7200 (bia 2c54.2d61.7200)
                              Internet address is 10.92.51.106/30
                              MTU 15080 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
                                 reliability 255/255, txload 1/255, rxload 1/255
                              Encapsulation ARPA, loopback not set
                              Keepalive not supported
                              Full Duplex, 1000Mbps, link type is force-up, media type is T
                              output flow-control is on, input flow-control is on
                              ARP type: ARPA, ARP Timeout 04:00:00
                              Last input 00:00:00, output 02:45:36, output hang never
                              Last clearing of "show interface" counters never
                              Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
                              Queueing strategy: Class-based queueing
                              Output queue: 0/40 (size/max)
                              5 minute input rate 0 bits/sec, 0 packets/sec
                              FigabitEthernet0/0/8 is up, line protocol is up
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
                              Full Duplex, 1000Mbps, link type is auto, media type is T
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
                                 0 output buffer failures, 0 output buffers swapped out
                            """

        self.tree = """{
                            "id": "j1-2",
                            "text": "b1",
                            "icon": "icon1",
                            "rule_id":0,
                            "children": [
                                {
                                    "id": "j3-2",
                                    "text": "b2",
                                    "icon": "icon2",
                                    "rule_id": 2,
                                    "children": [
                                        {
                                            "id": "j3-3",
                                            "text": "d1",
                                            "icon": "icon3",
                                            "rule_id":4,
                                            "children": []
                                        },
                                        {
                                            "id": "j3-4",
                                            "text": "d2",
                                            "icon": "icon4",
                                            "rule_id": 1000054,
                                            "children": []
                                        },
                                        {
                                            "id": "j3-5",
                                            "text": "d3",
                                            "icon": "icon5",
                                            "rule_id": 1000055,
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }"""

        self.tree_id = "j3-3"

        request_dict = {
            'data': self.raw_data,
            'tree': json.loads(self.tree),
            'tree_id': self.tree_id
        }

        render = Render(**request_dict)
        html_data = render.render()
        # f = open(r'C:\Users\yangyuan\Desktop\D2\apolo\ntt W\text1.html', 'w')
        # f.write(html_data)
        # f.close()
        return html_data

