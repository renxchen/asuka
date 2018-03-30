#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: snmp_collection_test.py
@time: 2018/3/29 14:21
@desc:

"""
from rest_framework import viewsets
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback


class SnmpCollectionTest(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(SnmpCollectionTest, self).__init__(**kwargs)
        self.request = request
        method = 'GET'
        self.snmp_oid = views_helper.get_request_value(self.request, 'snmp_oid', method)

    def get(self):
        try:
            pass
            data = {
                'data': {
                    'data': [],
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
