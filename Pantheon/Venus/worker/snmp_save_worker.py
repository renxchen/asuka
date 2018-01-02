# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from units import save_snmp
import threading
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class SaveFileWorker(WorkerBase):
    name = "snmpSaveFile"
    channels = 'snmpSaveFile'

    def handler(self, task_id, task, logger):
        try:
            params = task['params']
            save_snmp(params)
        except Exception, e:
            print str(e)
        return {}


main(SaveFileWorker)
