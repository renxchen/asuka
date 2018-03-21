#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: device_export.py
@time: 2018/03/08 14:19
@desc:

"""
from backend.apolo.serializer.devices_groups_serializer import DevicesSerializer, DevicesGroupsSerializer
from backend.apolo.models import Devices
from backend.apolo.tools import constants
from rest_framework.views import APIView
from rest_framework import viewsets
from backend.apolo.apolomgr.resource.device import groups_views
from backend.apolo.tools.views_helper import api_return
from django.core.paginator import Paginator
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
from itertools import chain
import simplejson as json
from django.db import transaction
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
import csv, codecs, re
import string
import time
from django.http import HttpResponse
from backend.apolo.apolomgr.resource.common import csv_export
import csv, os


class ExportDevicesViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(ExportDevicesViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        method = 'GET'
        if request.method.lower() == 'get':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        # devices related parameters
        self.operation_id = views_helper.get_request_value(self.request, 'operation_id', method)
        self.group_name = views_helper.get_request_value(self.request, 'group_name', method)
        self.ostype_name = views_helper.get_request_value(self.request, 'ostype_name', method)
        self.data_list = views_helper.get_request_value(self.request, 'id_list', method)
        self.group_id = views_helper.get_request_value(self.request, 'group_id', method)
        self.hostname = views_helper.get_request_value(self.request, 'hostname', method)
        self.ip = views_helper.get_request_value(self.request, 'ip', method)
        self.telnet_port = views_helper.get_request_value(self.request, 'telnet_port', method)
        self.snmp_port = views_helper.get_request_value(self.request, 'snmp_port', method)
        self.snmp_community = views_helper.get_request_value(self.request, 'snmp_community', method)
        self.snmp_version = views_helper.get_request_value(self.request, 'snmp_version', method)
        self.login_expect = views_helper.get_request_value(self.request, 'login_expect', method)
        self.device_type = views_helper.get_request_value(self.request, 'device_type', method)
        self.telnet_status = views_helper.get_request_value(self.request, 'telnet_status', method)
        self.status_type = views_helper.get_request_value(self.request, 'status_type', method)

    def export(self):
        """@brief
        Get the data of Device table and generate csv with the
        right format that can be imported again
        @post return data of Device table
        @return: the csv file
        """
        try:
            queryset = Devices.objects.filter(status=1)
            header = [u'Hostname', u'IP Address', u'Telnet Port', u'SNMP Port', u'SNMP Community', u'SNMP Version',
                      u'Login Expect', u'Device Type', u'OS Type', u'Group']
            csv_data = []
            csv_data.insert(0, header)
            for i in queryset:
                row = []
                row.append(i.hostname)
                row.append(i.ip)
                row.append(i.telnet_port)
                row.append(i.snmp_port)
                row.append(i.snmp_community)
                row.append(i.snmp_version)
                row.append(i.login_expect)
                row.append(i.device_type)
                row.append(i.ostype.name)
                group = ''
                if i.devicesgroups_set.all().exists:
                    for devicegroup in i.devicesgroups_set.all():
                        group += devicegroup.group.name + ','
                if group != '':
                    row.append(group[:-1])
                else:
                    row.append(group)
                csv_data.append(row)
            script_dir = os.path.split(os.path.realpath(__file__))[0]
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))),
                                    constants.CSV_PATH)

            # create csv
            result = csv_export.csv_export(csv_path, csv_data)
            # download csv
            if result is False:
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: result
                    },
                }
                return api_return(data=data)
            return result

        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
