#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_view.py
@time: 2018/1/3 10:51
@desc:

'''
import traceback

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import viewsets

from backend.apolo.apolomgr.resource.common.common_policy_tree.tool import Tool
from backend.apolo.models import Schedules, Items
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
        #  v1/api_data_collection/?id=1
        # search conditions
        priority = views_helper.get_request_value(self.request, 'policy_type', 'GET')
        os_type = views_helper.get_request_value(self.request, 'os_type', 'GET')
        device_group = views_helper.get_request_value(self.request, 'device_group', 'GET')
        coll_policy_group = views_helper.get_request_value(self.request, 'coll_policy_group', 'GET')
        data_schedule_type = views_helper.get_request_value(self.request, 'data_schedule_type', 'GET')
        # start_datetime = views_helper.get_request_value(self.request, 'start_datetime', 'GET')
        # end_datetime = views_helper.get_request_value(self.request, 'end_datetime', 'GET')
        status =views_helper.get_request_value(self.request, 'status', 'GET')
        schedule_id = views_helper.get_request_value(self.request, 'id', 'GET')

        try:
            if schedule_id is not '':
               # edit page
               schedules_obj = Schedules.objects.get(schedule_id=schedule_id)
               schedules_dict = SchedulesSerializer(schedules_obj).data
               data_schedule_time = Tool.split_data_schedule_time(schedules_dict['data_schedule_time'])
               schedules_dict.update(data_schedule_time)
               schedules_dict['start_period_time'] = schedules_dict['start_period_time'].replace('@', ' ')
               schedules_dict['end_period_time'] = schedules_dict['end_period_time'].replace('@', ' ')
               data = {
                   'data': schedules_dict,
                   'new_token': self.new_token,
                   constants.STATUS: {
                       constants.STATUS: constants.TRUE,
                       constants.MESSAGE: constants.SUCCESS
                   }
               }
               return api_return(data=data)
            field_relation_ships = {
                'priority': 'priority',
                'data_schedule_type': 'data_schedule_type',
                'os_type': 'ostype__name',
                'coll_policy_group': 'coll_policy_groups__name',
                'device_group': 'groups__name',
                'status': 'status'
            }
            query_data = {
                'priority': priority,
                'status': status,
                'data_schedule_type': data_schedule_type,
                'ostype__name': os_type,
                'coll_policy_groups__name': coll_policy_group,
                'groups__name': device_group
            }
            search_fields = ['priority', 'ostype', 'device_group', 'coll_policy_group', 'data_schedule_type', 'status']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            total_num = len(Schedules.objects.all())
            if search_conditions:
                queryset = Schedules.objects.filter(**search_conditions).order_by(*sorts)
            else:
                queryset = Schedules.objects.all().order_by(*sorts)
            serializer = SchedulesSerializer(queryset, many=True)
            paginator = Paginator(serializer.data, int(self.max_size_per_page))
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
        # load data
        schedule_id = views_helper.get_request_value(self.request, 'id', 'GET')
        if not self.__update_recode_check__(schedule_id):
            data = {
                'new_token': self.new_token,
                constants.STATUS: {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.CAN_NOT_UPDATE_SCHEDULE_MESSAGE  # can not delete
                }
            }
            return api_return(data=data)
        else:
            pass


    def delete(self):
        # v1/api_data_collection/?id=1
        schedule_id = views_helper.get_request_value(self.request, 'id', 'GET')
        if not self.__delete_recode_check__(schedule_id):
            pass
        else:

            if not self.__delete_recode_check__():
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.CAN_NOT_DELETE_SCHEDULE_MESSAGE  # can not delete
                    }
                }
                return api_return(data=data)
            else:

                try:
                    with transaction.atomic():
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

    @staticmethod
    def __update_recode_check__(schedule_id):
        print schedule_id
        return True

    @staticmethod
    def __delete_recode_check__(schedule_id):
        print schedule_id
        return True







