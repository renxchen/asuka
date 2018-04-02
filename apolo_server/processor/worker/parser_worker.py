# -*- coding: utf-8 -*-
import sys
from worker_base import WorkerBase, main
from parser_helper import parser_main
from apolo_server.processor.trigger.trigger_helper import TriggerHelp
from apolo_server.processor.constants import ParserConstants, CommonConstants
import logging
import json
import time
import traceback
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class Parser(WorkerBase):
    name = "parser_trigger"
    channels = ('parser',)
    threads = 15

    def handler(self, task_id, task, data, logger):

        item_type = CommonConstants.CLI_TYPE_CODE if task["channel"].upper() == "CLI" \
                         else CommonConstants.SNMP_TYPE_CODE

        device_log_info = ""
        try:
            deviceinfo = task["device_info"]
            result = task["element_result"][data.strip()]
            device_log_info = "Device ID: %s,IP: %s,HostName: %s" % (deviceinfo["device_id"],deviceinfo["ip"],deviceinfo["hostname"])

            items,parser_result = parser_main(item_type,data,deviceinfo,result,device_log_info,self.logger)
            #print json.dumps(items, indent=2), timestamp
            #trigger = TriggerHelp(items, logger)
            #trigger.trigger(task_timestamp=time.time())
            result = dict(
                    result_type = "parser",
                    task_id=task_id,
                    #command=command,
                    parser_result=parser_result,
                    status="success",
                    message="",
                )
            if item_type == CommonConstants.CLI_TYPE_CODE:
                result.update(dict(command=data,parser_result=parser_result))
            else:
                result.update(dict(clock=data))

        except Exception, e:
            result = dict(
                result_type = "parser",
                task_id=task_id,
                status="fail",
                message=str(e)
            )
            if item_type == CommonConstants.CLI_TYPE_CODE:
                result.update(dict(command=data))
            else:
                result.update(dict(clock=data))

            logger.error(device_log_info+" "+str(e))
            print traceback.format_exc()
        return result


main(Parser)
