# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from apolo_server.processor.parser.parser_helper import parser_main
from apolo_server.processor.trigger.trigger_helper import TriggerHelp
import logging
import json
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class Parser(WorkerBase):
    name = "parser_trigger"
    channels = 'parser'
    threads = 20

    def handler(self, task_id, task, logger):
        result = {}
        try:
            params = task['params']
            item_type = params['item_type']
            items, timestamp = parser_main(item_type=item_type, params=params)
            trigger = TriggerHelp(items, logger)
            trigger.trigger(task_timestamp=timestamp)
            result = dict(
                task_id=task_id,
                status="success",
                message="",
            )
        except Exception, e:
            result = dict(
                task_id=task_id,
                status="fail",
                message=str(e)
            )
            logger.error(str(e))
        return result


main(Parser)
