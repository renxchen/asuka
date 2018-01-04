#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_serializer.py
@time: 2018/1/3 13:14
@desc:

'''
from rest_framework import serializers

from backend.apolo.models import Schedules


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ('schedule_id', 'valid_period_type', 'data_schedule_type', 'valid_period_time',
                  'data_schedule_time', 'priority', 'status', 'policy_group_name',
                  'device_group_name', 'ostype_name')

    def create(self, validated_data):
        return Schedules.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


