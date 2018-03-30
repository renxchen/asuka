#!/usr/bin/env python
# coding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: cli_collection_test.py
@time: 2018/3/29 14:21
@desc:

"""
from rest_framework import viewsets
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
import traceback
from apolo_server.processor.worker.cisco_cli_helper import CiscoCLI, LoginException
import simplejson as json


class CliCollectionTest(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CliCollectionTest, self).__init__(**kwargs)
        self.request = request
        # self.device_info = eval(views_helper.get_request_value(self.request, 'device_info', method))
        try:
            # self.device_info = eval(request.body).get('device_info')
            self.device_info = eval(self.request.POST.get('device_info'))
            self.device_info['start_default_commands'] = '，'.join(self.device_info['start_default_commands'])
            self.device_info['end_default_commands'] = '，'.join(self.device_info['end_default_commands'])
            self.device_info['fail_judges'] = '，'.join(self.device_info['fail_judges'])
            self.device_info['device_id'] = 1000
        except Exception as e:
            print traceback.format_exc(e)
            # self.start_default_commands = views_helper.get_request_value(self.request, 'start_default_commands', method)
            # self.end_default_commands = views_helper.get_request_value(self.request, 'end_default_commands', method)
            # self.promet = views_helper.get_request_value(self.request, 'prompt', method)
            # self.fail_judges = views_helper.get_request_value(self.request, 'fail_judges', method)
            # self.ip = views_helper.get_request_value(self.request, 'ip', method)
            # self.hostname = views_helper.get_request_value(self.request, 'hostname', method)
            # self.expect = views_helper.get_request_value(self.request, 'expect', method)
            # self.device_id = views_helper.get_request_value(self.request, 'device_id', method)
            # self.timeout = views_helper.get_request_value(self.request, 'timeout', method)
            # self.device_info = {
            #     "commands": self.commands,
            #     "start_default_commands": '，'.join(self.start_default_commands),
            #     "end_default_commands": '，'.join(self.end_default_commands),
            #     "prompt": self.promet,
            #     "fail_judges": '，'.join(self.fail_judges),
            #     "ip": self.ip, "hostname": self.hostname,
            #     "expect": self.expect,
            #     "timeout": self.timeout,
            #     'device_id': self.device_id
            # }

    def test(self):
        # import logging
        # log_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # formatter = logging.Formatter(log_pattern)
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # ch.setFormatter(formatter)
        # logger = logging.getLogger("CiscoCli.log")
        # logger.setLevel(logging.DEBUG)
        # logger.addHandler(ch)


        import logging
        import time
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        time_stamp = time.time()
        handler = logging.FileHandler(
            "/home/apolo/project/apolo/backend/apolo/apolomgr/resource/collection_test_case/CiscoCli_" + str(
                time_stamp) + ".log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

        worker = CiscoCLI(self.device_info, logger=logger)
        output = []
        output_log = ''
        try:
            worker.login()
            commands = self.device_info['commands']
            for index, cmd in enumerate(commands):
                try:
                    cmd_out = worker.execute(cmd)
                    output.append(cmd_out)
                except LoginException as e:
                    if e.err_code == LoginException.LOGIN_TIMEOUT:
                        worker.recover_prompt()
                    else:
                        raise
            worker.exe_end_default_command()
            f = open(
                "/home/apolo/project/apolo/backend/apolo/apolomgr/resource/collection_test_case/CiscoCli_" + str(
                    time_stamp) + ".log")
            contents = f.readlines()
            output_log = chr(10).join(contents)
            f.close()
        except Exception as e:
            logger.error(e)
            print traceback.format_exc(e)
        finally:
            worker.close()

        return output, output_log

    def post(self):
        try:
            output, output_log = self.test()
            data = {
                'data': {
                    'data': output,
                    'log': output_log,
                },
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
