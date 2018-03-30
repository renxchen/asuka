#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: groups_views.py
@time: 2018/02/10 16:55
@desc:

"""

from backend.apolo.serializer.data_collection_serializer import DeviceGroupIDNameSerializer, OstypeSerializer
from backend.apolo.models import Groups, Ostype, Schedules, DevicesGroups
from backend.apolo.apolomgr.resource.device import device_views, ostype_views
from backend.apolo.tools import constants
from rest_framework import viewsets
from backend.apolo.tools.views_helper import api_return
from django.core.paginator import Paginator
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
import simplejson as json
from django.forms.models import model_to_dict
from django.db import transaction


class GroupsViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(GroupsViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        method = 'GET'
        if request.method.lower() == 'get':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        # groups related parameters
        self.group_id = views_helper.get_request_value(self.request, 'group_id', method)
        self.name = views_helper.get_request_value(self.request, 'name', method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        self.ostype_id = views_helper.get_request_value(self.request, 'ostype_id', method)

    @staticmethod
    def get_group(kwargs):
        """@brief
        get the data of the Groups table
        @param kwargs: the condition to query the table
        @pre call when need to get the data of Groups table
        @post return the data when queryset exits and False when queryset not exit
        @return: the data when queryset exits and False when queryset not exit
        """
        try:
            return Groups.objects.get(**kwargs)
        except Groups.DoesNotExist:
            return False

    @staticmethod
    def get_ostype(kwargs):
        """@brief
        get the data of the Ostype table
        @param kwargs: the condition to query the table
        @pre call when need to get the data of Ostype table
        @post return the data when queryset exits and exception string when queryset not exit
        @return: the data when queryset exits and exception string when queryset not exit
        """
        try:
            ostype_info = Ostype.objects.get(**kwargs)
            return ostype_info
        except Exception, e:
            return exception_handler(e)

    def get(self):
        """@brief
        get the data of Groups table
        @return: the data of Groups table
        """
        try:
            queryset = Groups.objects.all()
            # return name&ostype for checking whether they can be changed
            name = ""
            ostype = ""
            if self.group_id:
                query_conditions = {'group_id': self.group_id}
                queryset_device = device_views.DevicesViewSet.get_device_group(query_conditions)
                if queryset_device.exists():
                    ostype = False
                    name = False
                else:
                    ostype = True
                    name = True
                queryset = Groups.objects.filter(**query_conditions)
                if not queryset.exists():
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.GROUP_NOT_EXIST
                        }
                    }
                    return api_return(data=data)
            serializer = DeviceGroupIDNameSerializer(queryset, many=True)
            data = {
                'data': serializer.data,
                'new_token': self.new_token,
                'verify_result': {
                    "name": name,
                    "ostype": ostype,
                    "desc": "true"
                },
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            print e
            raise e

    def post(self):
        """@brief
        create a new group
        @return: the created group when create success and error when create fail
        """
        if "," in self.name:
            data = {
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.GROUP_NAME_FORMAT_ERROR
                }
            }
            return api_return(data=data)
        kwargs_groupname = {'name': self.name}
        groups = self.get_group(kwargs_groupname)
        if groups:
            data = {
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.GROUP_ALREADY_EXISTS
                }
            }
            return api_return(data=data)
        kwargs_ostypeid = {"ostypeid": self.ostype_id}
        ostype = self.get_ostype(kwargs_ostypeid)
        ostype_id = ostype.ostypeid
        ostype = model_to_dict(ostype)
        try:
            with transaction.atomic():
                data = {
                    'name': self.name,
                    'desc': self.desc,
                    'ostype': ostype,
                }
                serializer = DeviceGroupIDNameSerializer(data=data)
                if serializer.is_valid(Exception):
                    serializer.save(ostype_id=ostype_id)
                    data = {
                        'data': serializer.data,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            print e
            raise e

    def put(self):
        """@brief
        modify a group
        @return: the modified group when modify success and error when modify fail
        """
        try:
            with transaction.atomic():
                if self.name:
                    kwargs_groupname = {'name': self.name}
                    groups = self.get_group(kwargs_groupname)
                    if groups:
                        if int(groups.group_id) != int(self.group_id):
                            data = {
                                'new_token': self.new_token,
                                constants.STATUS: {
                                    constants.STATUS: constants.FALSE,
                                    constants.MESSAGE: constants.GROUP_ALREADY_EXISTS
                                }
                            }
                            return api_return(data=data)
                if "," in self.name:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.GROUP_NAME_FORMAT_ERROR
                        }
                    }
                    return api_return(data=data)
                kwargs_group = {'group_id': self.group_id}
                group = self.get_group(kwargs_group)
                kwargs_ostype = {'ostypeid': self.ostype_id}
                ostype = self.get_ostype(kwargs_ostype)
                if not isinstance(ostype, str):
                    data = {
                        'name': self.name,
                        'desc': self.desc,
                        'ostype': ostype.__dict__,
                    }
                else:
                    data = {
                        'name': self.name,
                        'desc': self.desc
                    }
                if group is False:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.GROUP_NOT_EXIST
                        }
                    }
                    return api_return(data=data)
                serializer = DeviceGroupIDNameSerializer(group, data=data, partial=True)
                if serializer.is_valid(Exception):
                    if not isinstance(ostype, str):
                        serializer.save(ostype_id=ostype.ostypeid)
                    else:
                        serializer.save()
                    data = {
                        'data': serializer.data,
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                    return api_return(data=data)
                else:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: serializer.errors
                        }
                    }
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            print e
            raise e


    def delete(self):
        """@brief
        delete a group
        @return: the success when delete success and error when delete fail
        """
        try:
            with transaction.atomic():
                if self.group_id:
                    kwards_schedules = {'device_group_id': self.group_id}
                    queryset_schedules = Schedules.objects.filter(**kwards_schedules)
                    if queryset_schedules.count() != 0:
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.EXISTS_IN_SCHEDULES
                            }
                        }
                        return api_return(data=data)
                    kwards_devicegroup = {'group_id': self.group_id}
                    queryset_device = DevicesGroups.objects.filter(**kwards_devicegroup)
                    if queryset_device.count() != 0:
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.EXISTS_IN_DEVICESGROUPS
                            }
                        }
                        return api_return(data=data)
                    queryset = self.get_group({'group_id': self.group_id})
                    if queryset:
                        queryset.delete()
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.TRUE,
                                constants.MESSAGE: constants.SUCCESS
                            }
                        }
                        return api_return(data=data)
                    else:
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.GROUP_NOT_EXIST
                            }
                        }
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            print e
            raise e

