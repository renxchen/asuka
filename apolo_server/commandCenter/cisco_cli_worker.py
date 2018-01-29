# -*- coding: utf-8 -*-

__version__ = 0.1
__author__ = 'zhutong <zhtong@cisco.com>'

from cisco_cli_helper import CiscoCLI
from worker_base import WorkerBase, main


class CiscoCliWorker(WorkerBase):
    name = 'CiscoCli'        
    channels = 'ios', 'nxos', 'iox', 'mds', 'asa'

    def handler(self, task_id, task, logger):
        device_info = task['device_info']
        commands = task['commands']
        given_name = device_info.get('hostname')
        output = []

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
                output.append(cmd_out)
        except Exception as e:
            status = 'fail'
            message = str(e)
            hostname = given_name
        finally:
            worker.close()

        return dict(status=status,
                    task_id=task_id,
                    ip=device_info['ip'],
                    hostname=hostname,
                    message=message,
                    output=output)


# main(CiscoCliWorker)
