#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: necwang
@contact: necwang@cisco.com
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
from backend.apolo.tools import views_helper
import logging
import time


class CliCollectionTest(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CliCollectionTest, self).__init__(**kwargs)
        self.request = request
        # self.device_info = eval(views_helper.get_request_value(self.request, 'device_info', method))
        # self.device_info = eval(request.body).get('device_info')
        method = 'BODY'
        if request.method.lower() == 'get' or request.method.lower() == 'delete':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.device_info = {}
        self.commands = views_helper.get_request_value(self.request, 'commands', method)
        self.start_default_commands = views_helper.get_request_value(self.request, 'start_default_commands', method)
        self.end_default_commands = views_helper.get_request_value(self.request, 'end_default_commands', method)
        self.prompt = views_helper.get_request_value(self.request, 'prompt', method)
        self.port = views_helper.get_request_value(self.request, 'port', method)
        self.fail_judges = views_helper.get_request_value(self.request, 'fail_judges', method)
        self.ip = views_helper.get_request_value(self.request, 'ip', method)
        self.hostname = views_helper.get_request_value(self.request, 'hostname', method)
        self.expect = views_helper.get_request_value(self.request, 'expect', method)
        self.timeout = views_helper.get_request_value(self.request, 'timeout', method)
        self.SPILT_CHAT = u"，"
        self.integrate_data()

    def integrate_data(self):
        self.device_info['commands'] = self.commands.split(',')
        self.device_info['start_default_commands'] = self.SPILT_CHAT.join(self.start_default_commands.split(','))
        self.device_info['end_default_commands'] = self.SPILT_CHAT.join(self.end_default_commands.split(','))
        self.device_info['prompt'] = str(self.prompt)
        self.device_info['fail_judges'] = self.SPILT_CHAT.join(self.fail_judges.split(','))
        self.device_info['ip'] = str(self.ip)
        self.device_info['hostname'] = str(self.hostname)
        self.device_info['expect'] = str(self.expect)
        self.device_info['timeout'] = int(self.timeout)
        self.device_info['port'] = int(self.port)
        self.device_info['device_id'] = 1000

    def cli_work(self):
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
        for per in output:
            per['output'] = str(per['output']).replace('\r\n', '<br>')
        return output, output_log

    def post(self):
        try:
            output, output_log = self.cli_work()
            data = {
                'data': {
                    'data': output,
                    'log': output_log,
                },
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.PUT_SUCCESSFUL
                }
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
