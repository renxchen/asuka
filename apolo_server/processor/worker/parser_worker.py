# -*- coding: utf-8 -*-
import sys
from worker_base import WorkerBase, main
from parser_helper import ParserHelp
from apolo_server.processor.trigger.trigger_helper import TriggerHelp
from apolo_server.processor.constants import ParserConstants, CommonConstants
import logging
import json
import time
import traceback
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class Parser(WorkerBase):
    name = "parser"
    channels = ('parser',)
    threads = 10

    def handler(self, task_id, task, data, logger):

        device_log_info = ""
        result_type = "parser"
        try:

            if data == CommonConstants.ALL_FINISH_CHECK_FLAG:
                result_type = CommonConstants.ALL_FINISH_CHECK_FLAG
                #trigger = TriggerHelp(task,[],"",logger)
                #if "parser_result" in task:
                #    trigger.handle_complex_triggers(task["parser_result"])
                
                #trigger.cache_event()

                unhandle_triggers = []
                #db_events = trigger.db_events
                db_events=[]
                items = []

            else:
                clock = data                
                parser = ParserHelp(clock,self.logger)
                parser.parse(task,clock)
                items = parser.get_items()
                
                #trigger = TriggerHelp(task,items,clock,logger)
                #trigger.trigger()
                #unhandle_triggers = trigger.unhandle_triggers
                #db_events = trigger.db_events

                unhandle_triggers = []
                db_events=[]

            result = dict(
                    result_type = result_type,
                    task_id=task_id,
                    collection_clock=data,
                    unhandle_triggers = unhandle_triggers,
                    status="success",
                    message="",
                    items=items,
                    db_events=db_events

                )
        except Exception, e:
            result = dict(
                result_type = result_type,
                task_id=task_id,
                collection_clock=data,
                unhandle_triggers=[],
                status="fail",
                db_events=[],
                message=str(e)
            )
            logger.error(device_log_info+" "+str(e))
            print traceback.format_exc()
        return result

main(Parser)
