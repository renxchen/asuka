#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: device_pre_view.py
@time: 2018/03/06 14:19
@desc:

"""

from backend.apolo.serializer.devices_groups_serializer import DevicesTmpSerializer, DevicesGroupsSerializer
from backend.apolo.models import Groups, Ostype, DevicesTmp, DevicesGroups
from backend.apolo.tools import constants
from rest_framework.views import APIView
from rest_framework import viewsets
from backend.apolo.apolomgr.resource.device import groups_views, device_views
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
import string, copy
from multiprocessing.dummy import Pool as ThreadPool
import requests


class DevicePreViewSet(APIView):
    parser_classes = (FileUploadParser,)

    def __init__(self, request, **kwargs):
        super(DevicePreViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        method = 'GET'
        if request.method.lower() == 'get':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        # device pre related parameters
        self.data_list = views_helper.get_request_value(self.request, 'id_list', method)
        self.group_name = views_helper.get_request_value(self.request, 'group_name', method)
        self.ostype_name = views_helper.get_request_value(self.request, 'ostype', method)
        self.operation_id = views_helper.get_request_value(self.request, 'operation_id', method)
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

    @staticmethod
    def telnet_status_check(device_id):
        """@brief
        check the device_tmp status in Devive_Tmp table whether it can telnet success
        @param device_id: the device_id in Device_Tmp table to confirm the device which need to check
        @pre call when need to check the telnet_status
        @post return the telnet result with post Gin`s API
        @return: the telnet_status and device_id
        """
        device = DevicesTmp.objects.get(device_id=device_id)
        ostype = Ostype.objects.get(ostypeid=device.ostype_id)
        default_commands = ostype.start_default_commands
        time_out = ostype.telnet_timeout

        payload = {
            "commands": [
                "show version"
            ],
            "default_commands": default_commands,
            "ip": device.ip,
            "platform": "ios",
            "expect": device.login_expect,
            "timeout": time_out,
            "task_timestamp": 1519796623,
            "method": "telnet"
        }
        r = requests.post("http://10.71.244.134:8080/api/v1/sync/cli", data=json.dumps(payload))
        response = json.loads(r.text)
        return response.get('status'), device_id

    @staticmethod
    def snmp_status_check(device_id):
        """@brief
        check the device_tmp status in Devive_Tmp table whether it can snmp success
        @param device_id: the device_id in Device_Tmp table to confirm the device which need to check
        @pre call when need to check the snmp_status
        @post return the snmp result with post Gin`s API
        @return: the snmp_status and device_id
        """
        device = DevicesTmp.objects.get(device_id=device_id)
        ostype = Ostype.objects.get(ostypeid=device.ostype_id)
        time_out = ostype.snmp_timeout
        payload = {
            "commands": {
                "operate": "bulk_get",
                "oids": [
                    "SNMPv2-MIB::sysObjectID.0"
                ]
            },
            "timeout": time_out,
            "ip": device.ip,
            "task_timestamp": 1519796765,
            "community": device.snmp_community
        }
        r = requests.post("http://10.71.244.134:8080/api/v1/sync/snmp", data=json.dumps(payload))
        response = json.loads(r.text)
        for x in response.get('output'):
            if 'message' in x.keys():
                if x.get('message').find('timeout') > -1:
                    return 'Fali', device_id
                else:
                    return 'Success', device_id
            else:
                return 'Success', device_id

    def get(self):
        """@brief
        get the data in Device_Tmp table by the operation_id
        @return: the data of Device_Tmp table
        """
        try:
            queryset_devices = DevicesTmp.objects.filter(operation_id=self.operation_id)
            field_relation_ships = {
                'hostname': 'hostname',
                'ip': 'ip',
                'telnet_port': 'telnet_port',
                'snmp_port': 'snmp_port',
                'snmp_community': 'snmp_community',
                'snmp_version': 'snmp_version',
                'login_expect': 'login_expect',
                'device_type': 'device_type',
                'telnet_status': 'telnet_status',
                'status_type': 'snmp_status',
                'group_name': 'group_name',
                'ostype': 'ostype',
            }
            query_data = {
                'hostname': self.hostname,
                'ip': self.ip,
                'telnet_port': self.telnet_port,
                'snmp_port': self.snmp_port,
                'snmp_community': self.snmp_community,
                'snmp_version': self.snmp_version,
                'login_expect': self.login_expect,
                'device_type': self.device_type,
                'telnet_status': self.telnet_status,
                'snmp_status': self.status_type,
                'group_name': self.group_name,
                'ostype': self.ostype_name,
            }
            search_fields = ['hostname', 'ip', 'telnet_port', 'snmp_port', 'snmp_community', 'snmp_version',
                             'login_expect', 'device_type', 'telnet_status', 'status_type', 'group_name', 'ostype']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            if sorts != []:
                if 'ostype' in sorts:
                    sorts = ['ostype__name' if x == 'ostype' else x for x in sorts]
                if '-ostype' in sorts:
                    sorts = ['-ostype__name' if x == '-ostype' else x for x in sorts]
            else:
                sorts = ['device_id']
            if search_conditions:
                ostype_condition = search_conditions.get('ostype__contains')
                if ostype_condition is not None:
                    ostype_list = Ostype.objects.filter(**{"name__contains": ostype_condition})
                    queryset_devices = queryset_devices.filter(**{'ostype__in': ostype_list})
                    del search_conditions['ostype__contains']
                queryset_devices = queryset_devices.filter(**search_conditions).order_by(*sorts)
            else:
                queryset_devices = queryset_devices.order_by(*sorts)
            serializer = DevicesTmpSerializer(queryset_devices, many=True)
            paginator = Paginator(serializer.data, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': contacts.object_list,
                'operation_id': self.operation_id,
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                'page_range': list(paginator.page_range),
                'page_has_next': contacts.has_next(),
                'total_num': len(queryset_devices),
                'current_page_num': contacts.number,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            print e
            raise e

    def put(self):
        """@brief
        check and change the status of telnet and snmp in Device_Tmp table by the list of device_id
        @return: the status of check result
        """
        try:
            with transaction.atomic():
                data_list = self.data_list
                data_return = []
                # telnet test
                pool = ThreadPool(device_views.CLI_THREADPOOL_SIZE)
                res_telnet = pool.map(self.telnet_status_check, data_list)
                pool.close()
                pool.join()
                for x in res_telnet:
                    device_pre = DevicesTmp.objects.get(device_id=x[1])
                    telnet_res = x[0]
                    data = {
                        'telnet_status': telnet_res,
                    }
                    serializer = DevicesTmpSerializer(device_pre, data=data, partial=True)
                    if serializer.is_valid(Exception):
                        serializer.save()
                # snmp test
                pool = ThreadPool(device_views.CLI_THREADPOOL_SIZE)
                res_snmp = pool.map(self.snmp_status_check, data_list)
                pool.close()
                pool.join()

                for x in res_snmp:
                    device_pre = DevicesTmp.objects.get(device_id=x[1])
                    snmp_res = x[0]
                    data = {
                        'snmp_status': snmp_res,
                    }
                    serializer = DevicesTmpSerializer(device_pre, data=data, partial=True)
                    if serializer.is_valid(Exception):
                        serializer.save()
                    data_return.append(serializer.data)
                data = {
                    'data': data_return,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                }
                return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            print e
            raise e
