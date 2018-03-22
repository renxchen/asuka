import sys
from apolo_server.processor.parser.common_policy_tree.dispatch import Dispatch
from apolo_server.processor.constants import ParserConstants, CommonConstants
from apolo_server.processor.parser.common_policy_tree.tool import Tool
from apolo_server.processor.db_units.memcached_helper import ItemMemCacheDb, RulesMemCacheDb
from apolo_server.processor.db_units.db_helper import ParserDbHelp
from multiprocessing.dummy import Pool as ThreadPool
import threading
import json
import os
import logging
import time
import thread

"""
class Parser(object):
    def __init__(self, items, result):
        self.items = items
        #self.timestamp = 0
        #self.items = []
        self.get_param_from_request(items,result)

    def get_param_from_request(self, param):
        
        #self.parser_params['rules'] = rules
        #self.parser_params['items'] = param['items']
        #self.timestamp = param['task_timestamp']
        for item in self.parser_params['items']:
            #self.items.append(item)
            item['task_timestamp'] = param['task_timestamp'] if "task_timestamp" in param else 0

    def handle(self):
        pass

    def send_request(self):
        pass
"""

class SNMPParser(object):
    def __init__(self):
        pass
        
    def handle(self,items,result):

        output = result["output"]
        clock = result["clock"]
        #result = []
        #parser_result = {}
        #timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        ParserDbHelp().bulk_save_result(items,clock, CommonConstants.SNMP_TYPE_CODE)
        return ""


class CliParser(object):

    
    def __init__(self):
       
        pass
        #super(CliParser, self).__init__(param)
       

    def handle(self,items,result):
        
        rules = {}
        with RulesMemCacheDb() as rules:
            rules = rules.get()
        #print rules

        output = result["output"]
        clock = result["clock"]
        #result = []
        parser_result = {}
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        for item in items:
            rule_path = CliParser.__split_path(item['tree_path'],
                                               item['rule_id'])
            #raw_data = item['output']
            #if raw_data is None:
            #continue
            p = Dispatch(rule_path, rules, output)
            p.dispatch()
            arry = p.get_result()
            item['value'] = arry[-1][0]
            parser_result[str(item['item_id'])] = {"value":item['value']}
            
        ParserDbHelp().bulk_save_result(items, clock, CommonConstants.CLI_TYPE_CODE)
        return parser_result

    @staticmethod
    def __split_path(path, rule_id):
        rules = []
        if len(path) == 1:
            rules.append(rule_id)
        else:
            rules = path.split(ParserConstants.TREE_PATH_SPLIT)[1:]
            rules.append(rule_id)
        return [str(rule) for rule in rules]


def parser_main(item_type,task, data,result):

    deviceinfo = task["device_info"]
    result = task["element_result"][data.strip()]
    items = []

    time_prefix = ["1day","1hour","15min","5min","1min"]
    oid_dict = {}
    if item_type == CommonConstants.SNMP_TYPE_CODE:
        for data in result["output"]:
            oid_dict[data["origin_oid"]] = {"value":data["value"],"message":data["message"]}

    for prefix in time_prefix:
        itemkey = "items_%s" % prefix
        if itemkey  not in deviceinfo:
            continue
        
        for item in deviceinfo[itemkey]:

            if item_type == CommonConstants.SNMP_TYPE_CODE:
                if item["oid"] in oid_dict:
                    item.update(oid_dict[item["oid"]])
                    items.append(item)
            else:
                if item["command"] == data:
                    items.append(item)


    if item_type == CommonConstants.CLI_TYPE_CODE:
        func = CliParser()
    else:
        #pass
        func = SNMPParser()
    result = func.handle(items,result)
    return items,result
    #items = __wrapper(func.parser_params['items'])
    #return items, func.timestamp


if __name__ == "__main__":
    start_time = time.time()
    with open("test_cli_param.json") as f:
        test_cli_param = json.loads(f.read())

    #parser_main(0, test_cli_param)
    # items, timestamp = parser_main(item_type=0, params=test_cli_param)
    end_time = time.time()
    print end_time - start_time
    
    
    #pool = ThreadPool(20)
    #for i in range(0, 1000):
    #    pool.apply_async(parser_main, args=(0, test_cli_param))
    #pool.close()
    #pool.join()
    # trigger = TriggerHelp(items, logging)
    # trigger.trigger(task_timestamp=123)
    # cli_handle = CliParser(test_cli_param)
    # cli_handle.handle()
    # with open("test_snmp_param.json") as f:
    #     test_snmp_param = json.loads(f.read())
    # snmp_handle = SNMPParser(test_snmp_param)
    # snmp_handle.handle()