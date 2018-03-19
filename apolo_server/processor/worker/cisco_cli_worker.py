# -*- coding: utf-8 -*-

__version__ = 0.1
__author__ = 'zhutong <zhtong@cisco.com>'
import  sys
sys.path.append("/Users/yihli/Desktop/projects/apolo")
from cisco_cli_helper import CiscoCLI
from worker_base import WorkerBase, main
import json

class CiscoCliWorker(WorkerBase):
    name = 'CiscoCli'        
    channels = ('cli',)

    def handler(self, task_id, task, logger,message):
        device_info = task['device_info']
        commands = []
        #"cmd_5min": ["show interface","show clock"],   
        #"cmd_15min":["show version","show clock"],
        #"cmd_1hour":["show version"],
        #"cmd_1day":["show version"],
        for key in ["cmd_1day","cmd_1hour","cmd_15min","cmd_5min"]:
            if key in device_info:
                if not commands:
                    commands.extend(device_info[key])
                else:
                    for cmd in device_info[key]:
                        if cmd not in commands:
                            commands.append(cmd)

        print commands
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
            for cmd in commands:
                cmd_out = worker.execute(cmd)
                #output.append(cmd_out)
                #cmd_out.update("result_type","command")
                cmd_out.update(dict(result_type="command_result", task_id=task_id))
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
                    result_type="task"
                    )


main(CiscoCliWorker)
