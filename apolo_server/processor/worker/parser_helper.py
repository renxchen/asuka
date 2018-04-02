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
    ParserDbHelp().bulk_save_result(items,clock, CommonConstants.SNMP_TYPE_CODE)
    return ""

def cli_parse(items,result,device_log_info,logger):

        output = result["output"]
        clock = result["clock"]
        parser_result = {}
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        for item in items:
            p = Dispatch(item["rule_path"], item["rules"], output)
            p.dispatch()
            arry = p.get_result()

            if arry[-1][0]["extract_match_flag"]:
                value = arry[-1][0]['extract_data']
                if value:
                    value = value[0]
                else:
                    value = None

                item['data'] = {"value": value,"block_path":arry[-1][0]["block_path"]}
                parser_result[str(item['item_id'])] = item['data']
                item["parse_status"] = True
            else:
                item["parse_status"] = False
                logger.error("%s CLI PARSE ERROR, ITEM_ID:%s Error_Info:%s " % (device_log_info,['item_id'],arry[-1][0]["error_msg"]))

        ParserDbHelp().bulk_save_result([item for item in items if item["parse_status"] == True], clock, CommonConstants.CLI_TYPE_CODE)
        return parser_result

def parser_main(item_type,data,deviceinfo, result,device_log_info,logger):

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
        result = cli_parse(items,result,device_log_info,logger)
        items = [item for item in items if item["parse_status"] == True]
    else:
        #pass
        result = snmp_parse(items,result,device_log_info,logger)
    #result = func.handle(items,result)
    return items,result

if __name__ == "__main__":
    pass