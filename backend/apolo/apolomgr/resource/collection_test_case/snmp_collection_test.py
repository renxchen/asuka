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
from apolo_server.processor.worker.snmp_helper import SNMP, chunks
import simplejson as json
import logging
import time

class SnmpCollectionTest(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(SnmpCollectionTest, self).__init__(**kwargs)
        self.request = request
        self.ip = self.request.GET['ip']
        self.community = self.request.GET['community']
        self.oids = eval(self.request.GET['oids'])

    def test(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        time_stamp = time.time()
        path = "/home/apolo/project/apolo/backend/apolo/apolomgr/resource/collection_test_case/snmp_result_" + str(
            time_stamp)
        handler = logging.FileHandler(path + ".log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        device_log_info = "Device ID: 1000,IP: 10.71.244.135,HostName: crs1000"
        worker = SNMP(self.ip,
                      self.community,
                      logger=logger,
                      port=161,
                      timeout=5,
                      retries=2,
                      device_log_info=device_log_info,
                      model_version=1,
                      is_translate=True
                      )
        try:
            # oids = ['1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.2.0']
            oids = self.oids
            maxvars = 20
            snmp_fun = worker.bulk_get
            if len(oids) > maxvars:
                _oid_splits = chunks(oids, maxvars)
            else:
                _oid_splits = [oids]
            fw = open(path, "w")
            output = []
            for _oids in _oid_splits:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                clock = time.time()
                result = snmp_fun(_oids)
                result.update(dict(result_type="element_result", timestamp=timestamp, clock="%f" % clock))
                fw.write(json.dumps(result, indent=2))
                output.append(result)
            fw.close()
            return output
        except Exception as e:
            logger.error(e)
            f = open(path + ".log")
            contents = f.readlines()
            exception_log = chr(10).join(contents)
            f.close()
            print traceback.format_exc(e)
            return exception_log

    def get(self):
        try:
            output = self.test()
            data = {
                'data': {
                    'data': output,
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
