# -*- coding: utf-8 -*-

__version__ = 0.1
__author__ = 'zhutong <zhtong@cisco.com>'

from worker_base import WorkerBase, main
from cisco_cli_helper import CiscoCLI, LoginException
import json
import traceback


class CiscoCliWorker(WorkerBase):
    name = 'CiscoCli'
    channels = ('cli',)
    threads = 10

    def handler(self, task_id, task, data, logger):
        device_info = task['device_info']
        commands = []

        command_dict = {}
        for key in ["items_1day", "items_1hour", "items_15min", "items_5min", "items_1min"]:
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

        given_name = device_info.get('hostname')
        worker = CiscoCLI(device_info, logger=logger)
        device_log_info = worker.device_log_info

        logger.info('%s Telnet Collection Start' % device_log_info)
        try:
            worker.login()
            for cmd in commands:
                try:
                    cmd_out = worker.execute(cmd)
                    cmd_out.update(dict(result_type="element_result",
                                        task_id=task_id, item_ids=command_dict[cmd]))
                    self.zmq_push.send(json.dumps(cmd_out))
                except LoginException as e:
                    if e.err_code == LoginException.LOGIN_TIMEOUT:
                        worker.recover_prompt()
                    else:
                        raise

            worker.exe_end_default_command()
            status = "success"
            message = ""

        except Exception as e:
            status = 'fail'
            message = str(e)
            logger.error(e)
            print traceback.format_exc()

        finally:
            worker.close()

        logger.info('%s Telnet Collection Finish' % device_log_info)
        return dict(status=status,
                    task_id=task_id,
                    # ip=device_info['ip'],
                    device_id=device_info['device_id'],
                    hostname=given_name,
                    message=message,
                    channel=task['channel'],
                    result_type="task_result"
                    )


main(CiscoCliWorker)
