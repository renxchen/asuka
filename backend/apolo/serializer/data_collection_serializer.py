#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_serializer.py
@time: 2018/1/3 13:14
@desc:

'''
from rest_framework import serializers

from backend.apolo.models import Schedules, CollPolicyGroups, Groups, Items


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ('schedule_id', 'valid_period_type', 'data_schedule_type', 'start_period_time',
                  'end_period_time', 'period_time', 'data_schedule_time', 'priority', 'status',
                  'policy_group_name', 'device_group_name', 'ostype_name',)

class SchedulesAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class CollPolicyGroupIDNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollPolicyGroups
        fields = ('policy_group_id', 'name',)
        # fields = '__all__'

class DeviceGroupIDNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ('group_id', 'name',)
        # fields = '__all__'