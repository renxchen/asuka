import sys
#from apolo_server.processor.parser.common_policy_tree.dispatch
from apolo_server.processor.db_units.db_units import *
from backend.apolo.apolomgr.resource.common.common_policy_tree.dispatch import Dispatch
from apolo_server.processor.constants import ParserConstants, CommonConstants
#from apolo_server.processor.parser.common_policy_tree.tool import Tool
from apolo_server.processor.db_units.memcached_helper import ItemMemCacheDb, RulesMemCacheDb
from apolo_server.processor.db_units.db_helper import ParserDbHelp
from multiprocessing.dummy import Pool as ThreadPool
import threading
import json
import os
import logging
import time
import thread


class SNMPParser(object):
    def __init__(self):
        pass
        
    def handle(self,items,result):

        output = result["output"]
        clock = result["clock"]
        ParserDbHelp().bulk_save_result(items,clock, CommonConstants.SNMP_TYPE_CODE)
        return ""


class CliParser(object):

    def __init__(self):
        pass
        #super(CliParser, self).__init__(param)
       
    def handle(self,items,result):
        rules = {}
        #with RulesMemCacheDb() as rules:
        #rules = rules.get()
        #print rules
        #trigger_detail

        output = result["output"]
        clock = result["clock"]
        #result = []
        parser_result = {}
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        for item in items:
            #rule_path = CliParser.__split_path(item['tree_path'],
            #                               item['rule_id'])
            #raw_data = item['output']
            #if raw_data is None:
            #continue
            p = Dispatch(item["rule_path"], item["rules"], output)
            p.dispatch()
            arry = p.get_result()

            value = arry[-1][0]['extract_data']
            if len(value) == 0:
                value = None
            else:
                value = value[0]

            item['data'] = {"value": value,"block_path":arry[-1][0]["block_path"]}
            #item['value'] = "test%s"%item['item_id']
            parser_result[str(item['item_id'])] = item['data']
            
        ParserDbHelp().bulk_save_result(items, clock, CommonConstants.CLI_TYPE_CODE)
        return parser_result



def parser_main(item_type,task, data):

    deviceinfo = task["device_info"]
    result = task["element_result"][data.strip()]
    items = []

    time_prefix = ["1day","1hour","15min","5min","1min"]
    oid_dict = {}

    status = result.get("status","")
    message = result.get("message","")
    if status!= "success":
        raise Exception(message)

    if item_type == CommonConstants.SNMP_TYPE_CODE:
        for data in result["output"]:
            oid_dict[data["origin_oid"]] = {"status":data["status"],"value":data["value"]}
  
    for prefix in time_prefix:
        itemkey = "items_%s" % prefix
        if itemkey  not in deviceinfo:
            continue
        
        for item in deviceinfo[itemkey]:

            if item_type == CommonConstants.SNMP_TYPE_CODE:
                tmp_oid_dict = oid_dict[item["oid"]]
                status = tmp_oid_dict.get("status","")
                if status != "success":
                    continue

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
    pass