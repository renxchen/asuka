# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from units import save_snmp
import threading
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class TriggerWorker(WorkerBase):
    name = "trigger"
    channels = 'trigger'

    def handler(self, task_id, task, logger):
        try:
            params = task['params']
            policy_id = params['policy_id']
        except Exception, e:
            print str(e)
        return {}