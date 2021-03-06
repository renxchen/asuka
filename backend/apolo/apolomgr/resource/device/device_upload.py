#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: device_upload.py
@time: 2017/03/06 14:19
@desc:

"""
from backend.apolo.serializer.devices_groups_serializer import DevicesTmpSerializer
from backend.apolo.models import Groups, Ostype, DevicesTmp
from backend.apolo.tools import constants
from rest_framework.views import APIView
from backend.apolo.apolomgr.resource.device import groups_views
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
from django.db import transaction
from rest_framework.parsers import FileUploadParser
import csv, codecs, re
import string
import time
import chardet


class DevicePreViewSet(APIView):
    parser_classes = (FileUploadParser,)

    def __init__(self, request, **kwargs):
        super(DevicePreViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')

    def post(self):
        """@brief
        check the upload csv file format and save the data with the right format in the Device_Tmp table
        @return: the list of the error upload format and mark the wrong style of the field
        """
        try:
            with transaction.atomic():
                import os
                line1 = "Hostname,IP Address,Telnet Port,SNMP Port,SNMP Community,SNMP Version,Login Expect,Device Type,OS Type,Group\r\n"
                line2 = "\xef\xbb\xbfHostname,IP Address,Telnet Port,SNMP Port,SNMP Community,SNMP Version,Login Expect,Device Type,OS Type,Group\r\n"
                filename = self.request.FILES['file']

                for index, line in enumerate(filename):
                    if index == 0:
                        # when the uploaded file title doesn`t contains ',',return the wrong csv format
                        if ',' not in line:
                            data = {
                                'data': [],
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.CSV_FORMAT_ERROR
                                },
                            }
                            return api_return(data=data)
                        # if the title is not in line1(utf-8) or line2(utf-8 with bom),the title is wrong
                        if line == line1:
                            hostname = "Hostname"
                        elif line == line2:
                            hostname = "\xef\xbb\xbfHostname"
                        else:
                            data = {
                                'data': [],
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.CSV_TITLE_ERROR
                                },
                            }
                            return api_return(data=data)
                    # if the code is not in follow codes , the code of file is wrong
                    if chardet.detect(line).get('encoding') not in ['ISO-8859-1', 'ascii', 'UTF-8-SIG', 'utf-8', 'Windows-1252']:
                        data = {
                            'data': [],
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.CSV_CODE_ERROR
                            },
                        }
                        return api_return(data=data)
                    if chardet.detect(line).get('encoding') in ['ISO-8859-1', 'ascii', 'UTF-8-SIG', 'utf-8']:
                        file_encode = 'utf-8'
                    else:
                        file_encode = 's_jisx0213'
                        break
                filename.open()
                dialect = csv.Sniffer().sniff(codecs.EncodedFile(filename, "utf-8", file_encode, errors="ignore").read(1024))
                filename.open()
                reader = csv.DictReader(codecs.EncodedFile(filename, "utf-8", file_encode, errors="ignore"), delimiter=',',
                                        dialect=dialect)
                headers = reader.fieldnames
                error_list = []
                file_x = []
                operation_id = int(time.time())
                file_dir = os.path.abspath(os.path.join(os.getcwd(), "upload"))
                if os.path.exists(file_dir):
                    pass
                else:
                    os.mkdir(file_dir)
                path_csv = os.path.abspath(os.path.join(file_dir, str(operation_id) + "_" + filename.name))
                hostname_dict = {}
                hostname_repetition = []
                for f in reader:
                    if len(f) != 10:
                        data = {
                            'data': [],
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.CSV_FORMAT_ERROR
                            },
                        }
                        return api_return(data=data)
                    file_x.append(f)
                    # hostname check
                    if f.get(hostname).strip() != '':
                        if hostname_dict.get(f.get(hostname)) is None:
                            hostname_dict[f.get(hostname)] = 0
                        else:
                            hostname_repetition.append(f.get(hostname))
                    else:
                        data = {
                            'data': [],
                            'error_list': error_list,
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.CSV_HOSTNAME_EMPTY
                            },
                        }
                        return api_return(data=data)
                if len(hostname_repetition) != 0:
                    data = {
                        'data_duplicate': list(set(hostname_repetition)),
                        'error_list': error_list,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.CSV_HOSTNAME_DUPLICATE
                        },
                    }
                    return api_return(data=data)
                with open(path_csv, 'ab+') as f:
                    writer = csv.DictWriter(f, headers)
                    writer.writeheader()
                    writer.writerows(file_x)
                group_list = Groups.objects.all()
                ostype_list = Ostype.objects.all()
                for f in file_x:
                    flag_err = 0
                    dict_check = {}
                    # hostname check
                    hostname_csv = f.get(hostname)
                    if len(hostname_csv) > 30:
                        dict_check['hostname_check'] = False
                        flag_err += 1
                    else:
                        for letter in hostname_csv:
                            if not (str(letter).isalnum() or (str(letter) in string.punctuation and str(letter) != ' '
                                                              and str(letter) != r"'" and str(letter) != "\""
                                                              and str(letter) != r",")):
                                dict_check['hostname_check'] = False
                                flag_err += 1
                                break
                            else:
                                dict_check['hostname_check'] = True
                    dict_check['hostname'] = hostname_csv
                    # ipv4 check
                    ip = f.get('IP Address')
                    pattern_ip = "^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$"
                    if re.match(pattern_ip, ip) is None:
                        dict_check['ip'] = False
                        flag_err += 1
                    else:
                        dict_check['ip'] = True
                    # telnet port check
                    telnet_port = f.get('Telnet Port')
                    try:
                        telnet_port = int(telnet_port)
                        if telnet_port < 0 or telnet_port > 65535:
                            dict_check['telnet_port'] = False
                            flag_err += 1
                        else:
                            dict_check['telnet_port'] = True
                    except ValueError:
                        dict_check['telnet_port'] = False
                        flag_err += 1
                    # snmp port check
                    snmp_port = f.get('SNMP Port')
                    try:
                        snmp_port = int(snmp_port)
                        if snmp_port < 0 or snmp_port > 65535:
                            dict_check['snmp_port'] = False
                            flag_err += 1
                        else:
                            dict_check['snmp_port'] = True
                    except ValueError:
                        dict_check['snmp_port'] = False
                        flag_err += 1
                    # snmp community check
                    snmp_community = f.get('SNMP Community')
                    if snmp_community == '':
                        dict_check['snmp_community'] = True
                    elif len(snmp_community) > 30:
                        dict_check['snmp_community'] = False
                        flag_err += 1
                    else:
                        for letter in snmp_community:
                            if not (str(letter).isalnum() or str(letter) in string.punctuation or str(letter) == ' '):
                                dict_check['snmp_community'] = False
                                flag_err += 1
                                break
                            else:
                                dict_check['snmp_community'] = True
                    # snmp version
                    snmp_version = f.get('SNMP Version')
                    if snmp_version == '':
                        dict_check['snmp_version'] = True
                    else:
                        if snmp_version != 'v1' and snmp_version != 'v2c':
                            dict_check['snmp_version'] = False
                            flag_err += 1
                        else:
                            dict_check['snmp_version'] = True
                    # login expect
                    login_expect = str(f.get('Login Expect'))
                    if login_expect == '':
                        dict_check['login_expect'] = True
                    elif len(login_expect) > 1000:
                        dict_check['login_expect'] = False
                        flag_err += 1
                    else:
                        flag_expect = 0
                        for letter in login_expect:
                            if not (str(letter).isalnum() or str(letter) in string.punctuation or str(
                                    letter) == ' '):
                                flag_expect += 1
                        if flag_expect > 0:
                            dict_check['login_expect'] = False
                            flag_err += 1
                        else:
                            dict_check['login_expect'] = True
                    # Device Type
                    device_type = f.get('Device Type')
                    if device_type == '':
                        dict_check['device_type'] = True
                    elif len(device_type) > 30:
                        dict_check['device_type'] = False
                        flag_err += 1
                    else:
                        flag_type = 0
                        for letter in device_type:
                            if not (str(letter).isalnum() or str(letter) in string.punctuation or str(letter) == ' '):
                                flag_type += 1
                        if flag_type > 0:
                            dict_check['device_type'] = False
                            flag_err += 1
                        else:
                            dict_check['device_type'] = True
                    # OS Type
                    ostype = f.get('OS Type')
                    flag_ostype = 0
                    if ostype != '':
                        for os in ostype_list:
                            if os.name == ostype:
                                dict_check['ostype'] = True
                                flag_ostype += 1
                        if flag_ostype == 0:
                            dict_check['ostype'] = False
                            flag_err += 1
                    else:
                        dict_check['ostype'] = False
                        flag_err += 1
                    # Group
                    group = f.get('Group')
                    group_res = ''
                    if group != '':
                        group = group.split(',')
                        if len(group) > 5:
                            dict_check['group'] = False
                            flag_err += 1
                        else:
                            flag_group = 0
                            group = list(set(group))
                            for group_one in group_list:
                                for g in group:
                                    if g == group_one.name:
                                        ostype_id = group_one.ostype_id
                                        if f.get('OS Type') == groups_views.GroupsViewSet.get_ostype(
                                                {"ostypeid": ostype_id}).name:
                                            flag_group += 1
                            if not flag_group == len(group):
                                dict_check['group'] = False
                                dict_check['ostype'] = False
                                flag_err += 1
                            else:
                                dict_check['group'] = True
                                for g in group:
                                    group_res = group_res + g + ','
                    else:
                        dict_check['group'] = True
                    if group_res != '':
                        group_res = group_res[:-1]
                    if flag_err > 0:
                        error_list.append(dict_check)
                    else:
                        ostype = groups_views.GroupsViewSet.get_ostype({'name': f.get('OS Type')})
                        valid_device = {
                            'operation_id': operation_id,
                            'hostname': f.get(hostname),
                            'ip': f.get('IP Address'),
                            'telnet_port': int(f.get('Telnet Port')),
                            'snmp_port': int(f.get('SNMP Port')),
                            'snmp_community': f.get('SNMP Community'),
                            'snmp_version': f.get('SNMP Version'),
                            'login_expect': f.get('Login Expect'),
                            'status': 1,
                            'telnet_status': 'No Data',
                            'snmp_status': 'No Data',
                            'device_type': f.get('Device Type'),
                            'group_name': group_res,
                            'ostype': ostype.__dict__
                        }
                        serializer = DevicesTmpSerializer(data=valid_device)
                        if serializer.is_valid(Exception):
                            serializer.save(ostype_id=ostype.ostypeid)
                data = {
                    'operation_id': operation_id,
                    'error_list': error_list,
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                }
                return api_return(data=data)
        except Exception, e:
            print e
            raise e
