import sys

from apolo_server.processor.db_units.db_units import *
from backend.apolo.apolomgr.resource.common.common_policy_tree.dispatch import Dispatch
from apolo_server.processor.constants import ParserConstants, CommonConstants
from apolo_server.processor.db_units.db_helper import ParserDbHelp
from multiprocessing.dummy import Pool as ThreadPool
import threading
import json
import os
import logging
import time
import thread



def snmp_parse(items,result,device_log_info,logger):
    output = result["output"]
    clock = result["clock"]
    ParserDbHelp().bulk_save_result([item for item in items if item["status"] == "success"],clock, CommonConstants.SNMP_TYPE_CODE)
    #return "",""

def cli_parse(items,result,device_log_info,logger):

        output = result["output"]
        clock = result["clock"]
        parser_result = {}
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        result_items=[]
        
        for item in items:
            if item["status"] != "success":
                continue
           
            p = Dispatch(item["rule_path"], item["rules"], output)
            p.dispatch()
            arry = p.get_result()
            item_id = item['item_id']

            if arry[-1][0]["extract_match_flag"]:
                value = arry[-1][0]['extract_data']
                if value:
                    value = value[0]
                else:
                    value = None
                item['value'] = value
                item["block_path"] = arry[-1][0]["block_path"]
            else:
                item["status"] = "parser_fail"
                logger.error("%s CLI PARSE ERROR, ITEM_ID:%d Error_Info:%s " % (device_log_info,item_id,arry[-1][0]["error_msg"]))
           

            
            del item["rules"]
            del item["rule_path"]
            
            #result_items.append(result_item)
        ParserDbHelp().bulk_save_result([item for item in items if item["status"] == "success"], clock, CommonConstants.CLI_TYPE_CODE)
        #return result_items

def parser_main(task,clock,device_log_info,logger):

    result = task["element_result"][clock]
    item_type = CommonConstants.CLI_TYPE_CODE if task["channel"].upper() == "CLI" \
                         else CommonConstants.SNMP_TYPE_CODE

    items = []
    time_prefix = ["1day","1hour","15min","5min","1min"]
    oid_dict = {}

    status = result.get("status","")
    message = result.get("message","")
    deviceinfo = task["device_info"]

    if status!= "success":
        raise Exception(message)

    if item_type == CommonConstants.SNMP_TYPE_CODE:
        for data in result["output"]:
            oid_dict[data["origin_oid"]] = {"status":data["status"],"value":data["value"],"message":data["message"]}
  
    for _prefix in time_prefix:
        _itemkey = "items_%s" % _prefix
        if _itemkey  not in deviceinfo:
            continue
        
        for item in deviceinfo[_itemkey]:

            if item_type == CommonConstants.SNMP_TYPE_CODE:
                tmp_oid_dict = oid_dict[item["oid"]]
                status = tmp_oid_dict.get("status","")
                #if status != "success":
                #    continue
                if item["oid"] in oid_dict:
                    item.update(oid_dict[item["oid"]])
                    items.append(item)
    
            else:
                if item["command"] == result["command"]:
                    #if result["status"] in "success coll_fail":
                    item["message"] = result["message"]
                    item["status"] = result["status"]
                    items.append(item)


    if item_type == CommonConstants.CLI_TYPE_CODE:
        cli_parse(items,result,device_log_info,logger)
        #items = [item for item in items if item["parse_status"] == True]
    else:
        #pass
        snmp_parse(items,result,device_log_info,logger)
    #result = func.handle(items,result)
    #print items
    return items

if __name__ == "__main__":
    pass