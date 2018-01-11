# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from Pantheon.Venus.trigger.trigger_helper import bulk_trigger
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class TriggerWorker(WorkerBase):
    name = "trigger"
    channels = 'trigger'
    threads = 15

    def handler(self, task_id, task, logger):
        try:
            params = task['params']
            # policy_id = params['policy_id']
            # device_id = params['device_id']
            items = params['items']
            clock = params['task_timestamp']
            bulk_trigger(items, clock)
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

main(TriggerWorker)