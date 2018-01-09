# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from Pantheon.Venus.parser.common_policy_tree.parser_help import parser_main
import json
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class Parser(WorkerBase):
    name = "parser"
    channels = 'parser'
    threads = 20

    def handler(self, task_id, task, logger):
        result = {}
        try:
            params = task['params']
            item_type = params['item_type']
            parser_main(item_type=item_type, params=params)
            # devices_info = get_items(now_time, item_type)
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
        return result


main(Parser)
