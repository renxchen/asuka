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
from rest_framework import viewsets

from backend.apolo.models import Schedules
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
        # /v1/api_data_collection/
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
        id = views_helper.get_request_value(self.request, 'id', 'GET')

        try:
            if id is not '':
               print id
               queryset= Schedules.objectss.filter(schedule_id=id)
               serializer = SchedulesSerializer(queryset, many=True)
               data = {
                   'data': serializer.data,
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






