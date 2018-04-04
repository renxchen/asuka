# -*- coding: utf-8 -*-

__version__ = 0.1
__author__ = 'zhutong <zhtong@cisco.com>'

import sys
from worker_base import WorkerBase, main
from cisco_cli_helper import CiscoCLI,LoginException
import json



class CiscoCliStatusWorker(WorkerBase):
    name = 'CiscoCli_Status_Check'        
    channels = ('status_cli',)
    threads = 5

    def handler(self, task_id, task, data, logger):
        device_info = task['device_info']
        given_name = device_info.get('hostname')

        worker = CiscoCLI(device_info, logger=logger)
        try:
            worker.login(default_command=False)
           
            status="success"
            message = ""

        except Exception as e:
            status = 'fail'
            message = str(e)
            logger.error(e)
            
        finally:
            worker.close()

        return dict(status=status,
                    task_id=task_id,
                    #ip=device_info['ip'],
                    device_id=device_info['device_id'],
                    message=message,
                    result_type=self.channels[0]
                    )

main(CiscoCliStatusWorker)
