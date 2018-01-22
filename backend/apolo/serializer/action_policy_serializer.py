#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: action_policy_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import DataTable, Schedules, DataTableItems


class ActionPolicyDataTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTable
        fields = '__all__'

    def create(self, validated_data):
        return DataTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.descr = validated_data.get('descr', instance.descr)
        instance.save()
        return instance


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ('schedule_id', 'valid_period_type', 'data_schedule_type', 'start_period_time',
                  'end_period_time', 'period_time', 'data_schedule_time', 'priority', 'status', 'policy_group',
                  'device_group', 'policy_group_name', 'device_group_name', 'ostype_name',)


class ActionPolicyDataTableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTableItems
        fields = '__all__'

    def create(self, validated_data):
        return DataTableItems.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.data_table_items_id = validated_data.get('data_table_items_id', instance.data_table_items_id)
        instance.table = validated_data.get('table', instance.table)
        instance.item = validated_data.get('item', instance.item)
        instance.save()
        return instance
