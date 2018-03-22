# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from apolo_server.processor.parser.parser_helper import parser_main
from apolo_server.processor.trigger.trigger_helper import TriggerHelp
from apolo_server.processor.constants import ParserConstants, CommonConstants
import logging
import json
import time
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class Parser(WorkerBase):
    name = "parser_trigger"
    channels = 'parser'
    threads = 20

    def handler(self, task_id, task, data, logger):

        #result = {}
        if not data:
            logger.error("miss parser data")
            return 

                
        item_type = CommonConstants.CLI_TYPE_CODE if task["channel"].upper() == "CLI" \
                         else CommonConstants.SNMP_TYPE_CODE

        try:
            #params = task['params']
            #item_type = params['item_type']
            items,parser_result = parser_main(item_type=item_type, task=task,data=data result=result)
            #print json.dumps(items, indent=2), timestamp
            trigger = TriggerHelp(items, logger)
            trigger.trigger(task_timestamp=time.time())
            result = dict(
                    result_type = "parser",
                    task_id=task_id,
                    command=command,
                    parser_result=parser_result,
                    status="success",
                    #message="",
                )
            if item_type == CommonConstants.CLI_TYPE_CODE:
                result.update(dict(command=command,parser_result=parser_result))
                
            else:
                result.update(dict(clock=data))

        except Exception, e:
            result = dict(
                result_type = "parser",
                task_id=task_id,
                status="fail",
                #command=command,
                message=str(e)
            )
            if item_type == CommonConstants.CLI_TYPE_CODE:
                result.update(dict(command=command))
            else:
                result.update(dict(clock=data))

            logger.error(str(e))
        return result


main(Parser)
