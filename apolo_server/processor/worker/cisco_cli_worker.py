# -*- coding: utf-8 -*-

__version__ = 0.1
__author__ = 'zhutong <zhtong@cisco.com>'

import sys
from ..constants import SYS_PATH
sys.path.append(SYS_PATH)
from cisco_cli_helper import CiscoCLI
from worker_base import WorkerBase, main
import json


class CiscoCliWorker(WorkerBase):
    name = 'CiscoCli'        
    channels = ('cli',)
    threads = 15

    def handler(self, task_id, task, data, logger):
        device_info = task['device_info']
        commands = []

        command_dict = {}
        for key in ["items_1day","items_1hour","items_15min","items_5min","items_1min"]:
            if key in device_info:
                for item in device_info[key]:
                    item_id = item["item_id"]
                    command = item["command"]
                    
                    if command in command_dict:
                        command_dict[command].append(item_id)
                    else:
                        command_dict[command] = [item_id]

                    if command not in commands:
                        commands.append(command)

        #print commands
        #commands = task['commands']

        given_name = device_info.get('hostname')
        #output = []

        #return dict(command=command, status=status, output=output, timestamp=timestamp)
        print device_info
        worker = CiscoCLI(device_info, logger=logger)
        try:
            worker.login()
            hostname = worker.hostname
            if given_name and given_name != hostname:
                message = 'Hostname not match. Given: %s, Got: %s' % (given_name, hostname)
                raise Exception(message)
            else:
                status = 'success'
                message = ''
            for index,cmd in enumerate(commands):
                cmd_out = worker.execute(cmd)
                
                """
                if index == 0:
                    first_element = True
                else:
                    first_element = False
                
                if index == len(commands)-1:
                    next_element = -1
                else:
                    next_element = commands[index]
                """
                
                cmd_out.update(dict(result_type="element_result",task_id=task_id,item_ids=command_dict[cmd]))
                self.zmq_push.send(json.dumps(cmd_out))


        except Exception as e:
            status = 'fail'
            message = str(e)
            hostname = given_name
        finally:
            worker.close()

        return dict(status=status,
                    task_id=task_id,
                    #ip=device_info['ip'],
                    device_id=device_info['device_id'],
                    #hostname=hostname,
                    message=message,
                    channel=task['channel'],
                    result_type="task_result"
                    )


main(CiscoCliWorker)
