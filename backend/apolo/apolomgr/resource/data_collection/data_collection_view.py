#!/usr/bin/env python

'''

@author: Gin Chen
@contact: Gin Chen@cisco.com
@file: data_collection_view.py
@time: 2018/1/3 10:51
@desc:

'''
import time
import traceback

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.tool import Tool
from backend.apolo.apolomgr.resource.data_collection.data_collection import DataCollectionOptCls
from backend.apolo.models import Schedules, Items, DataTableItems
from backend.apolo.serializer.data_collection_serializer import SchedulesSerializer
from backend.apolo.tools import views_helper, constants
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return


class DataCollectionViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataCollectionViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')

    def get(self):

        # v1/api_data_collection/?page=1&rows=10&sidx=status&sord=desc
        # v1/api_data_collection/?page=1&rows=10&status=3
        # v1/api_data_collection/?id=1
        # search conditions
        # priority = views_helper.get_request_value(self.request, 'policy_type', 'GET')
        os_type = views_helper.get_request_value(self.request, 'ostype_name', 'GET')
        device_group = views_helper.get_request_value(self.request, 'device_group_name', 'GET')
        coll_policy_group = views_helper.get_request_value(self.request, 'policy_group_name', 'GET')
        priority = views_helper.get_request_value(self.request, 'priority', 'GET')
        start_period_time = views_helper.get_request_value(self.request, 'start_period_time', 'GET')
        end_period_time = views_helper.get_request_value(self.request, 'end_period_time', 'GET')
        data_schedule_type = views_helper.get_request_value(self.request, 'data_schedule_type', 'GET')
        status = views_helper.get_request_value(self.request, 'schedules_is_valid', 'GET')
        schedule_id = views_helper.get_request_value(self.request, 'id', 'GET')
        sort_by = views_helper.get_request_value(self.request, 'sidx', 'GET')
        order = views_helper.get_request_value(self.request, 'sord', 'GET')
        try:
            if schedule_id is not '':
                # edit page
                schedules_obj = Schedules.objects.get(schedule_id=schedule_id)
                schedules_dict = SchedulesSerializer(schedules_obj).data
                data_schedule_time = Tool.split_data_schedule_time(schedules_dict['data_schedule_time'])
                schedules_dict.update(data_schedule_time)
                if schedules_dict['start_period_time']:
                    schedules_dict['start_period_time'] = schedules_dict['start_period_time'].replace('@', ' ')
                else:
                    schedules_dict['start_period_time'] = None
                if schedules_dict['end_period_time']:
                    schedules_dict['end_period_time'] = schedules_dict['end_period_time'].replace('@', ' ')
                else:
                    schedules_dict['end_period_time'] = None
                if not schedules_dict['policy_group_id']:
                    schedules_dict['policy_group_id'] = -1

                item_list = self.__get_items_list(schedule_id)
                is_processing = self.__check_is_Processing(item_list)
                is_lock = self.__check_is_lock(item_list)
                data = {
                    'data': schedules_dict,
                    'new_token': self.new_token,
                    'isProcessing': is_processing,
                    'isLock': is_lock,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                return api_return(data=data)

            field_relation_ships = {
                'priority': 'priority',
                'data_schedule_type': 'data_schedule_type',
                'ostype_name': 'ostype__name',
                'start_period_time': 'start_period_time',
                'end_period_time': 'end_period_time',
                'policy_group_name': 'policy_group__name',
                'device_group_name': 'device_group__name'
            }
            query_data = {
                'priority': Tool.priority_mapping(priority),
                'data_schedule_type': Tool.schedule_type_mapping(data_schedule_type),
                'start_period_time': start_period_time.replace(' ', '@'),
                'end_period_time': end_period_time.replace(' ', '@'),
                'ostype__name': os_type,
                'policy_group__name': coll_policy_group,
                'device_group__name': device_group
            }
            search_fields = ['priority', 'ostype_name', 'device_group_name', 'policy_group_name', 'start_period_time',
                             'end_period_time', 'data_schedule_type']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)

            total_num = Schedules.objects.count()
            if search_conditions:
                queryset = Schedules.objects.filter(**search_conditions).values('schedule_id',
                                                                                'valid_period_type',
                                                                                'data_schedule_type',
                                                                                'start_period_time',
                                                                                'end_period_time',
                                                                                'data_schedule_time',
                                                                                'priority',
                                                                                'policy_group__name',
                                                                                'policy_group_id',
                                                                                'device_group__name',
                                                                                'device_group_id',
                                                                                'device_group__name',
                                                                                'ostype_id',
                                                                                'ostype__name', ).order_by(*sorts)
            else:
                queryset = Schedules.objects.all('schedule_id',
                                                 'valid_period_type',
                                                 'data_schedule_type',
                                                 'start_period_time',
                                                 'end_period_time',
                                                 'data_schedule_time',
                                                 'priority',
                                                 'policy_group__name',
                                                 'policy_group_id',
                                                 'device_group__name',
                                                 'device_group_id',
                                                 'device_group__name',
                                                 'ostype_id',
                                                 'ostype__name', ).order_by(*sorts)

            # process data
            result = self.__clean_data(list(queryset))
            if sort_by and sort_by == 'schedules_is_valid':
                if order:
                    # True: asc, False: desc
                    reverse = True
                    if order.strip().lower() == 'asc'.strip().lower():
                        reverse = False
                    result = sorted(result, key=lambda result: result[sort_by], reverse=reverse)
            # filter status
            result_list = []
            if status:
                schedule_status = Tool.schedule_status_mapping(status)
                for schedule_item in result:
                    if schedule_item['schedules_is_valid'] in schedule_status:
                        result_list.append(schedule_item)
                paginator = Paginator(result_list, int(self.max_size_per_page))
            else:
                paginator = Paginator(result, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': contacts.object_list,
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                'page_range': list(paginator.page_range),
                'page_has_next': contacts.has_next(),
                'total_num': total_num,
                'current_page_num': contacts.number,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        # request param
        ostype = views_helper.get_request_value(self.request, "ostype_id", 'BODY')
        priority = views_helper.get_request_value(self.request, "priority", 'BODY')
        device_group_id = int(views_helper.get_request_value(self.request, "device_group_id", 'BODY'))
        policy_group_id = int(views_helper.get_request_value(self.request, "policy_group_id", 'BODY'))
        valid_period_type = views_helper.get_request_value(self.request, "valid_period_type", 'BODY')
        start_period_time = views_helper.get_request_value(self.request, "start_period_time", 'BODY')
        end_period_time = views_helper.get_request_value(self.request, "end_period_time", 'BODY')
        data_schedule_type = views_helper.get_request_value(self.request, "data_schedule_type", 'BODY')
        weeks = views_helper.get_request_value(self.request, "weeks", 'BODY')
        data_schedule_time = views_helper.get_request_value(self.request, "data_schedule_time", 'BODY')
        # load data
        schedule_id = views_helper.get_request_value(self.request, 'schedule_id', 'BODY')
        is_lock = views_helper.get_request_value(self.request, 'is_lock', 'BODY')
        is_processing = views_helper.get_request_value(self.request, 'is_processing', 'BODY')

        param_dict = {
            "ostype": ostype,
            "priority": priority,
            "device_group_id": device_group_id,
            "policy_group_id": policy_group_id,
            "valid_period_type": valid_period_type,
            "start_period_time": start_period_time,
            "end_period_time": end_period_time,
            "data_schedule_type": data_schedule_type,
            "weeks": weeks,
            "data_schedule_time": data_schedule_time
        }

        try:
            opt = DataCollectionOptCls(**param_dict)
            new_dict = opt.set_schedule_data()
            if is_lock or is_processing:
                Schedules.objects.filter(schedule_id=schedule_id).update(**new_dict)
            else:
                with transaction.atomic():
                    Items.objects.filter(schedule=schedule_id).delete()
                    # judge status that is all functions off
                    obj = Schedules.objects.filter(schedule_id=schedule_id)
                    old_status = obj[0].status
                    # the new request that is all functions off
                    if policy_group_id == -1:
                        # the old schedule status is all functions off
                        if old_status == 0:
                            if obj[0].device_group == device_group_id:
                                obj.update(**new_dict)
                            else:
                                Schedules.objects.filter(device_group=obj[0].device_group).update(status=1)
                                obj.update(**new_dict)
                                Schedules.objects.filter(device_group=device_group_id).update(status=0)
                        else:
                            # the old schedule status chance to all functions off
                            obj.update(**new_dict)
                            Schedules.objects.filter(device_group=device_group_id).update(status=0)
                    else:

                        if old_status == 0:
                            # the old schedule status are chanced from all function off to all function on
                            Schedules.objects.filter(device_group=obj[0].device_group).update(status=1)
                            obj.update(**new_dict)
                        else:
                            obj.update(**new_dict)

                    devices = opt.get_devices()
                    policies = opt.get_coll_policies()
                    if opt.insert_data_check(devices, policies):
                       opt.insert_new_items(devices, schedule_id, policies)
                    else:
                        transaction.set_rollback(True)
                        data = {
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.POLICY_DEVICE_COMBINATION
                            }
                        }
                        return api_return(data=data)
            data = {
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
            }
            return api_return(data=data)
        except Exception as e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        # v1/api_data_collection/?id=1
        schedule_id = views_helper.get_request_value(self.request, 'id', 'GET')
        try:
            with transaction.atomic():
                # close all function off thought update status =1
                obj = Schedules.objects.get(schedule_id=schedule_id)
                all_function_status = obj.status
                # all function off is opened
                if all_function_status == 0:
                    device_group_id = obj.device_group
                    Schedules.objects.filter(device_group=device_group_id).update(status=1)
                # delete items table
                # delete schedule table
                Items.objects.filter(schedule_id=schedule_id).delete()
                Schedules.objects.get(schedule_id=schedule_id).delete()
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                return api_return(data=data)
        except Exception as e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def __delete_recode_check(self, schedule_id):
        if self.__check_is_lock(schedule_id):
            return False
        else:
            return False

    @staticmethod
    def __check_is_lock(arry):
        queryset = DataTableItems.objects.filter(item__in=arry)
        if queryset.count() > 0:
            return True
        else:
            return False

    @staticmethod
    def __check_is_Processing(arry):
        is_processing = False
        data = Tool.get_data_from_collection_server()
        for recoder in data:
            if recoder['valid_status']:
                if recoder['item_id'] in arry:
                    is_processing = True
                    break
            else:
                continue
        return is_processing

    @staticmethod
    def __get_items_list(schedule_id):
        queryset = Items.objects.filter(schedule=schedule_id).values('item_id')
        item_id_arry = []
        for item in queryset:
            item_id_arry.append(item['item_id'])
        return item_id_arry

    @staticmethod
    def __clean_data(arry):
        now_time = time.strftime('%Y-%m-%d@%H:%M:%S', time.localtime(time.time()))
        for i in range(len(arry)):
            item = arry[i]
            if item['valid_period_type'] == 0:
                arry[i]['schedules_is_valid'] = 1
            else:
                if item['start_period_time'] < now_time < item['end_period_time']:
                    arry[i]['schedules_is_valid'] = 1
                else:
                    arry[i]['schedules_is_valid'] = 0

            if item['start_period_time'] and item['end_period_time']:
                before = item['start_period_time'].replace('@', ' ')
                after = item['end_period_time'].replace('@', ' ')
                arry[i]['period_time'] = str(before) + '~' + str(after)

            if not item['policy_group__name']:
                arry[i]['policy_group__name'] = 'ALL FUNCTIONS OFF'
            arry[i]['ostype_name'] = arry[i]['ostype__name']
            arry[i]['policy_group_name'] = arry[i]['policy_group__name']
            arry[i]['device_group_name'] = arry[i]['device_group__name']

        return arry
