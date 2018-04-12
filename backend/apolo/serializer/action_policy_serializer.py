#!/usr/bin/env python
"""

@author: necwang
@contact: necwang@cisco.com
@file: action_policy_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import DataTable, Schedules, DataTableItems, Triggers, TriggerDetail, Actions


class ActionPolicyDataTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTable
        fields = '__all__'

    def create(self, validated_data):
        return DataTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.descr = validated_data.get('descr', instance.descr)
        instance.coll_policy = validated_data.get('coll_policy', instance.coll_policy)
        instance.groups = validated_data.get('groups', instance.groups)
        instance.tree = validated_data.get('tree', instance.tree)
        instance.policy_group = validated_data.get('policy_group', instance.policy_group)
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


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triggers
        fields = '__all__'

    def create(self, validated_data):
        return Triggers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.trigger_id = validated_data.get('trigger_id', instance.trigger_id)
        instance.name = validated_data.get('name', instance.name)
        instance.descr = validated_data.get('descr', instance.descr)
        instance.status = validated_data.get('status', instance.status)
        instance.value = validated_data.get('value', instance.value)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.trigger_type = validated_data.get('trigger_type', instance.trigger_type)
        instance.trigger_limit_nums = validated_data.get('trigger_limit_nums', instance.trigger_limit_nums)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.expression = validated_data.get('expression', instance.expression)
        instance.columnA = validated_data.get('columnA', instance.columnA)
        instance.columnB = validated_data.get('columnB', instance.columnB)
        instance.save()
        return instance


class TriggerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggerDetail
        fields = '__all__'

    def create(self, validated_data):
        return TriggerDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.trigger_detail_id = validated_data.get('trigger_detail_id', instance.trigger_detail_id)
        instance.expression = validated_data.get('expression', instance.expression)
        instance.itemA = validated_data.get('itemA', instance.itemA)
        instance.itemB = validated_data.get('itemB', instance.itemB)
        instance.device_id = validated_data.get('device_id', instance.device_id)
        instance.descr = validated_data.get('descr', instance.descr)
        instance.status = validated_data.get('status', instance.status)
        instance.trigger = validated_data.get('trigger', instance.trigger)
        instance.expression_view = validated_data.get('expression_view', instance.expression_view)
        return instance


class ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = '__all__'

    def create(self, validated_data):
        return Actions.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.action_id = validated_data.get('action_id', instance.action_id)
        instance.action_type = validated_data.get('action_type', instance.action_type)
        instance.action_name = validated_data.get('action_name', instance.action_name)
        instance.snmp_version = validated_data.get('snmp_version', instance.snmp_version)
        instance.snmp_oid = validated_data.get('action_id', instance.snmp_oid)
        instance.community = validated_data.get('community', instance.community)
        instance.ip_address = validated_data.get('ip_address', instance.ip_address)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.command = validated_data.get('command', instance.command)
        instance.agent_address = validated_data.get('agent_address', instance.agent_address)
        instance.oid = validated_data.get('oid', instance.oid)
        instance.message = validated_data.get('message', instance.message)
        instance.param = validated_data.get('param', instance.param)
        instance.script_path = validated_data.get('script_path', instance.script_path)
        instance.status = validated_data.get('status', instance.status)
        instance.trigger = validated_data.get('trigger', instance.trigger)
        return instance
