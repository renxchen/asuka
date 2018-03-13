#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: device_views.py
@time: 2018/03/01 14:19
@desc:

"""

from backend.apolo.serializer.devices_groups_serializer import DevicesSerializer,DevicesGroupsSerializer
from backend.apolo.models import DevicesGroups,Devices,Groups,Ostype,DevicesTmp
from backend.apolo.tools import constants
from rest_framework import viewsets
from backend.apolo.tools.views_helper import api_return
from django.core.paginator import Paginator
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
from itertools import chain
import simplejson as json
from django.db import transaction
from django.db.models.query import QuerySet
import requests
from multiprocessing.dummy import Pool as ThreadPool
from backend.apolo.apolomgr.resource.data_collection.data_collection import DataCollectionOptCls
from backend.apolo.apolomgr.resource.action_policy.action_policy_views import ActionPolicyViewSet
# from backend.apolo.apolomgr.resource.action_policy import action_policy_views
import collections
CLI_THREADPOOL_SIZE = 20
TIME_OUT = 5



class DevicesViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DevicesViewSet, self).__init__(**kwargs)
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
        self.group_name = views_helper.get_request_value(self.request, 'group_list', method)
        self.ostype_name = views_helper.get_request_value(self.request, 'ostype_name', method)
        self.data_list =views_helper.get_request_value(self.request, 'id_list', method)
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
        device = Devices.objects.get(device_id=device_id)
        default_commands = Ostype.objects.get(ostypeid=device.ostype_id).start_default_commands

        payload = {
                  "commands": [
                    "show version"
                  ],
                  "default_commands": default_commands,
                  "ip": device.ip,
                  "platform": "ios",
                  "expect": device.login_expect,
                  "timeout": TIME_OUT,
                  "task_timestamp": 1519796623,
                  "method": "telnet"
                }
        r = requests.post("http://10.71.244.134:8080/api/v1/sync/cli", data=json.dumps(payload))
        response = json.loads(r.text)
        return response.get('status'),device_id

    @staticmethod
    def snmp_status_check(device_id):
        device = Devices.objects.get(device_id=device_id)
        payload = {
                  "commands": {
                    "operate": "bulk_get",
                    "oids": [
                      "SNMPv2-MIB::sysObjectID.0"
                    ]
                  },
                  "timeout": 5,
                  "ip": device.ip,
                  "task_timestamp": 1519796765,
                  "community": device.snmp_community
                }
        r = requests.post("http://10.71.244.134:8080/api/v1/sync/snmp", data=json.dumps(payload))
        response = json.loads(r.text)
        for x in response.get('output'):
            if 'message' in x.keys():
                if x.get('message').find('timeout')>-1:
                    return 'fali', device_id
                else:
                    return 'success',device_id
            else:
                return 'success', device_id

    @staticmethod
    def __ostype_sort(letter):
        return letter.get('ostype').get('name')

    @staticmethod
    def get_device_group(kwargs):
        try:
            return DevicesGroups.objects.filter(**kwargs)
        except DevicesGroups.DoesNotExist:
            return False

    @staticmethod
    def get_device_all(kwargs):
        try:
            return Devices.objects.filter(**kwargs)
        except Devices.DoesNotExist:
            return False

    def get(self):
        try:
            devices_id = []
            if self.group_id != '':
                if self.group_id == "-1":
                    queryset_devices = DevicesGroups.objects.all()
                else:
                    kwargs_group = {'group_id': self.group_id}
                    queryset_devices = self.get_device_group(kwargs_group)

                for group in queryset_devices:
                    devices_id.append(group.device_id)
                kwargs_devices = {'device_id__in': devices_id}
                if self.group_id == "-1":
                    queryset_devices = Devices.objects.filter(status=1).exclude(**kwargs_devices)
                elif self.group_id != '':
                    queryset_devices = self.get_device_all(kwargs_devices)
            else:
                queryset_devices = Devices.objects.filter(status=1)
            field_relation_ships = {
                'hostname': 'hostname',
                'ip': 'ip',
                'telnet_port': 'telnet_port',
                'snmp_port': 'snmp_port',
                'snmp_community': 'snmp_community',
                'snmp_version': 'snmp_version',
                'login_expect': 'login_expect',
                'device_type':'device_type',
                'telnet_status':'telnet_status',
                'status_type':'snmp_status',
                'group_list':'group',
                'ostype_name':'ostype',
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
                'group': self.group_name,
                'ostype': self.ostype_name,
            }
            search_fields = ['hostname', 'ip', 'telnet_port', 'snmp_port', 'snmp_community', 'snmp_version',
                             'login_expect', 'device_type', 'telnet_status', 'status_type','group_list','ostype_name']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)

            if sorts != []:
                if 'ostype' in sorts:
                    sorts = ['ostype__name' if x == 'ostype' else x for x in sorts]
                if '-ostype' in sorts:
                    sorts = ['-ostype__name' if x == '-ostype' else x for x in sorts]
                if 'group' in sorts:
                    sorts = ['devicesgroups__group__name' if x == 'group' else x for x in sorts]
                if '-group' in sorts:
                    sorts = ['-devicesgroups__group__name' if x == '-group' else x for x in sorts]
            if search_conditions:
                condition_group = search_conditions.get('group__contains')
                if condition_group is not None:
                    groups = Groups.objects.filter(**{"name__contains":condition_group})
                    groupid_list =[]
                    for group_detail in groups:
                        groupid_list.append(group_detail.group_id)
                    devicesgroups = DevicesGroups.objects.filter(**{"group_id__in":groupid_list})
                    search_conditions['devicesgroups__in'] = devicesgroups
                    del search_conditions['group__contains']
                condition_ostype = search_conditions.get('ostype__contains')
                if condition_ostype is not None:
                    ostype_list = Ostype.objects.filter(**{"name__contains":condition_ostype})
                    oid_list = []
                    for ostype in ostype_list:
                        oid_list.append(ostype.ostypeid)
                    search_conditions['ostype_id__in'] = oid_list
                    del search_conditions['ostype__contains']
                queryset_devices = queryset_devices.filter(**search_conditions).order_by(*sorts)
            else:
                queryset_devices = queryset_devices.order_by(*sorts)
            paginator = Paginator(queryset_devices, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            serializer = DevicesSerializer(contacts.object_list, many=True)
            if self.group_id == '':
                return_list = []
                if len(serializer.data) != 0:
                    for index in serializer.data:
                        check_dict = {}
                        check_dict['devices_id'] = index['device_id']
                        check_dict['hostname'] = index['hostname']
                        check_dict['ip'] = index['ip']
                        check_dict['telnet_port'] = index['telnet_port']
                        check_dict['snmp_port'] = index['snmp_port']
                        check_dict['snmp_community'] = index['snmp_community']
                        check_dict['snmp_version'] = index['snmp_version']
                        check_dict['login_expect'] = index['login_expect']
                        check_dict['telnet_status'] = index['telnet_status']
                        check_dict['snmp_status'] = index['snmp_status']
                        check_dict['device_type'] = index['device_type']
                        check_dict['ostype_name'] = index['ostype']['name']
                        if len(index['devicesgroups_set']) != 0:
                            group_str = ''
                            for devicesgroups in index['devicesgroups_set']:
                                group_str = group_str + devicesgroups['group']['name'] + ','
                            check_dict['group_list'] = group_str[:-1]
                        else:
                            check_dict['group_list'] = []
                        return_list.append(collections.OrderedDict(check_dict))
            else:
                return_list = serializer.data
            data = {
                'data': return_list,
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
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        try:
            with transaction.atomic():
                devices = Devices.objects.filter(status=1)
                # device_group_change
                device_group_before = []
                for device in devices:
                    device_group_old = {}
                    groups = DevicesGroups.objects.filter(device_id=device.device_id)
                    device_group_old["device_id"] = device.device_id
                    group_id_list = []
                    if groups.exists():
                        for group in groups:
                            group_id_list.append(group.group_id)
                    device_group_old["group_old"] = group_id_list
                    device_group_before.append(device_group_old)
                #delete devicegroups
                DevicesGroups.objects.all().delete()
                # update
                devices_tmp = DevicesTmp.objects.filter(operation_id=self.operation_id)
                devicegroup_list = []
                insert_list = []
                group_list = []
                if len(devices) == 0:
                    for tmp in devices_tmp:
                        group_list.append((tmp.hostname,tmp.group_name))
                        tmp.device_id = None
                        insert_list.append(tmp)
                    Devices.objects.bulk_create(insert_list)
                    for device_group in group_list:
                        device_name, groups_name = device_group
                        if groups_name != '':
                            device_id = Devices.objects.get(hostname=device_name,status=1).device_id
                            groupnames = groups_name.split(',')
                            for group_name in groupnames:
                                group_id = Groups.objects.get(name=group_name).group_id
                                devicegroup = DevicesGroups(device_id=device_id, group_id=group_id)
                                devicegroup_list.append(devicegroup)
                    if len(device_group) != 0:
                        DevicesGroups.objects.bulk_create(devicegroup_list)
                else:
                    queryset = devices
                    for tmp in devices_tmp:
                        flag = 0
                        group_list.append((tmp.hostname, tmp.group_name))
                        for current in devices:
                            if tmp.hostname == current.hostname:
                                queryset = queryset.exclude(hostname=tmp.hostname)
                                data = {
                                    'hostname': tmp.hostname,
                                    'ip': tmp.ip,
                                    'telnet_port': tmp.telnet_port,
                                    'snmp_port': tmp.snmp_port,
                                    'snmp_community': tmp.snmp_community,
                                    'snmp_version': tmp.snmp_version,
                                    'login_expect': tmp.login_expect,
                                    'device_type': tmp.device_type,
                                    'telnet_status': tmp.telnet_status,
                                    'snmp_status': tmp.snmp_status,
                                    'status': 1,
                                    'ostype_id': tmp.ostype.ostypeid,
                                }
                                serializer = DevicesSerializer(current,data=data,partial=True)
                                if serializer.is_valid():
                                    serializer.save()
                            else:
                                flag += 1
                                if flag == len(devices):
                                    tmp.device_id = None
                                    insert_list.append(tmp)
                    queryset.update(status=0)
                    Devices.objects.bulk_create(insert_list)
                    for device_group in group_list:
                        device_name, groups_name = device_group
                        if groups_name != '':
                            device_id = Devices.objects.get(hostname=device_name,status=1).device_id
                            groupnames = groups_name.split(',')
                            for group_name in groupnames:
                                group_id = Groups.objects.get(name=group_name).group_id
                                devicegroup = DevicesGroups(device_id=device_id, group_id=group_id)
                                devicegroup_list.append(devicegroup)
                    if len(device_group) != 0:
                        DevicesGroups.objects.bulk_create(devicegroup_list)
                    device_group_now = []
                    for device in devices:
                        device_group_new = {}
                        groups = DevicesGroups.objects.filter(device_id=device.device_id)
                        device_group_new["device_id"] = device.device_id
                        group_id_list = []
                        if groups.exists():
                            for group in groups:
                                group_id_list.append(group.group_id)
                        device_group_new["group_new"] = group_id_list
                        device_group_now.append(device_group_new)
                    group_list = []

                    for i in device_group_before:
                        group_dict = {}
                        flag = 0
                        for j in device_group_now:
                            if j.get("device_id") == i.get("device_id"):
                                group_dict["device_id"] = j.get("device_id")
                                group_old_list = i.get("group_old")
                                group_new_list = j.get("group_new")
                                group_dict["add_device_group"] = [x for x in group_new_list if x not in group_old_list]
                                group_dict["del_device_group"] = [x for x in group_old_list if x not in group_new_list]
                                group_list.append(group_dict)
                                break
                            else:
                                flag += 1
                            if flag == len(device_group_now):
                                group_dict["device_id"] = i.get("device_id")
                                group_dict["add_device_group"] = []
                                group_dict["del_device_group"] = i.get("group_old")
                                group_list.append(group_dict)

                    for i in device_group_now:
                        group_dict = {}
                        flag = 0
                        for j in device_group_before:
                            if j.get("device_id") == i.get("device_id"):
                                break
                            else:
                                flag += 1
                            if flag == len(device_group_before):
                                group_dict["device_id"] = i.get("device_id")
                                group_dict["add_device_group"] = i.get("group_new")
                                group_dict["del_device_group"] = []
                                group_list.append(group_dict)
                    # for yuanyang check
                    data_check = {}
                    data_check["items"] = group_list
                    opt = DataCollectionOptCls(**data_check)
                    opt.update_items()
                    # for kim check
                    act = ActionPolicyViewSet(request=self.request)
                    act.regenerate_trigger_detail()
                data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)



    def put(self):
        try:
            with transaction.atomic():
                data_list = self.data_list
                data_return = []
                # telnet test
                pool = ThreadPool(CLI_THREADPOOL_SIZE)
                res_telnet = pool.map(self.telnet_status_check, data_list)
                pool.close()
                pool.join()
                for x in res_telnet:
                    device_pre = Devices.objects.get(device_id=x[1])
                    telnet_res = x[0]
                    data ={
                        'telnet_status': telnet_res,
                    }
                    serializer = DevicesSerializer(device_pre, data=data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                # snmp test
                pool = ThreadPool(CLI_THREADPOOL_SIZE)
                res_snmp = pool.map(self.snmp_status_check, data_list)
                pool.close()
                pool.join()

                for x in res_snmp:
                    device_pre = Devices.objects.get(device_id=x[1])
                    snmp_res = x[0]
                    data = {
                        'snmp_status': snmp_res,
                    }
                    serializer = DevicesSerializer(device_pre, data=data, partial=True)
                    if serializer.is_valid():
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
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
