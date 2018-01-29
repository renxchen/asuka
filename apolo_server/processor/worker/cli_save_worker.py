# -*- coding: utf-8 -*-
from worker_base import WorkerBase, main
from units import save_output_file
import threading
__version__ = 0.1
__author__ = 'Rubick <haonchen@cisco.com>'


class SaveFileWorker(WorkerBase):
    name = "cliSaveFile"
    channels = 'cliSaveFile'

    def handler(self, task_id, task, logger):
        try:
            params = task['params']
            save_output_file(params)
        except Exception, e:
            print str(e)
        return {}


main(SaveFileWorker)
