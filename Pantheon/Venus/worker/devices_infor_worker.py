# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from Venus.collection.collection_help import get_items
import json
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class GetItemInformation(WorkerBase):
    name = "getItem"
    channels = 'getItem'

    def handler(self, task_id, task, logger):
        result = {}
        try:
            params = task['params']
            now_time = params['now_time']
            item_type = params['item_type']
            devices_info = get_items(now_time, item_type)
            result = dict(
                status="success",
                output=devices_info,
                message="",
                task_id=task_id
            )
        except Exception, e:
            result = dict(
                status="success",
                output=[],
                message=str(e),
                task_id=task_id
            )

        return result


main(GetItemInformation)
