#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: data_collection_serializer.py
@time: 2018/1/3 13:14
@desc:

'''
from rest_framework import serializers
from collection_policy_serializer import OstypeSerializer
from backend.apolo.models import Schedules, CollPolicyGroups, Groups, Items, Ostype, DataTableHistoryItems, \
    DataTableItems


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ('schedule_id', 'valid_period_type', 'data_schedule_type', 'start_period_time',
                  'end_period_time', 'period_time', 'data_schedule_time', 'priority', 'schedules_is_valid',
                  'policy_group_name', 'policy_group_id', 'device_group_name', 'device_group_id',
                  'ostype_id', 'ostype_name',)

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
    ostype = OstypeSerializer(many=False)

    class Meta:
        model = Groups
        fields = ('group_id', 'name','desc','ostype')
        # fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        desc = validated_data.get('desc')
        ostype_id = validated_data.get('ostype_id')
        return Groups.objects.create(**{'name':name,'desc':desc,'ostype_id': ostype_id})

    def update(self, instance, validated_data):
        # print dir(instance)
        # print validated_data
        ostypeid = validated_data.get('ostype_id')
        if ostypeid is not None:
            ostype_conditions = {'ostypeid':validated_data.get('ostype_id')}
            ostype = Ostype.objects.get(**ostype_conditions)
        else:
            ostype = None
        name = validated_data.get('name')
        if name != '':
            instance.name = name
        instance.desc = validated_data.get('desc', instance.desc)
        if ostype:
            instance.ostype = ostype
        instance.save()
        return instance

class DataTableHistoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTableHistoryItems
        fields = '__all__'

class DataTableItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTableItems
        fields = '__all__'