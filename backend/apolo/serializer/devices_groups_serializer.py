#!/usr/bin/env python
"""

@author: kaixliu
@contact: kaixliu@cisco.com
@file: devices_groups_serializer.py
@time: 2018/03/07 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import DevicesGroups, Devices, DevicesTmp, Groups
from collection_policy_serializer import OstypeSerializer
from data_collection_serializer import DeviceGroupIDNameSerializer


class DevicesTmpSerializer(serializers.ModelSerializer):
    ostype = OstypeSerializer(many=False)

    class Meta:
        model = DevicesTmp
        fields = ('operation_id', 'device_id', 'hostname', 'ip', 'telnet_port', 'snmp_port', 'snmp_community', 'status',
                  'snmp_version', 'login_expect', 'telnet_status', 'snmp_status', 'device_type', 'group_name', 'ostype')

    def create(self, validated_data):
        return DevicesTmp.objects.create(**{
            'operation_id': validated_data.get('operation_id'),
            'hostname': validated_data.get('hostname'),
            'ip': validated_data.get('ip'),
            'telnet_port': validated_data.get('telnet_port'),
            'snmp_port': validated_data.get('snmp_port'),
            'snmp_community': validated_data.get('snmp_community'),
            'snmp_version': validated_data.get('snmp_version'),
            'login_expect': validated_data.get('login_expect'),
            'status': validated_data.get('status'),
            'telnet_status': validated_data.get('telnet_status'),
            'snmp_status': validated_data.get('snmp_status'),
            'device_type': validated_data.get('device_type'),
            'group_name': validated_data.get('group_name'),
            'ostype_id': validated_data.get('ostype_id')})

    def update(self, instance, validated_data):
        instance.telnet_status = validated_data.get('telnet_status', instance.telnet_status)
        instance.snmp_status = validated_data.get('snmp_status', instance.snmp_status)
        instance.save()
        return instance


class DevicesGroupsSerializer(serializers.ModelSerializer):
    group = DeviceGroupIDNameSerializer(many=False)

    # device = DevicesSerializer(many=False)

    class Meta:
        model = DevicesGroups
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'


class DevicesSerializer(serializers.ModelSerializer):
    devicesgroups_set = DevicesGroupsSerializer(many=True)
    ostype = OstypeSerializer(many=False)

    class Meta:
        model = Devices
        fields = '__all__'

    def create(self, validated_data):
        return Devices.objects.create(**{
            'hostname': validated_data.get('hostname'),
            'ip': validated_data.get('ip'),
            'telnet_port': validated_data.get('telnet_port'),
            'snmp_port': validated_data.get('snmp_port'),
            'snmp_community': validated_data.get('snmp_community'),
            'snmp_version': validated_data.get('snmp_version'),
            'login_expect': validated_data.get('login_expect'),
            'telnet_status': validated_data.get('telnet_status'),
            'snmp_status': validated_data.get('snmp_status'),
            'status': validated_data.get('status'),
            'device_type': validated_data.get('device_type'),
            'ostype_id': validated_data.get('ostype_id')})

    def update(self, instance, validated_data):
        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.telnet_port = validated_data.get('telnet_port', instance.telnet_port)
        instance.snmp_port = validated_data.get('snmp_port', instance.snmp_port)
        instance.snmp_version = validated_data.get('snmp_version', instance.snmp_version)
        instance.snmp_community = validated_data.get('snmp_community', instance.snmp_community)
        instance.login_expect = validated_data.get('login_expect', instance.login_expect)
        instance.status = validated_data.get('status', instance.status)
        instance.device_type = validated_data.get('device_type', instance.device_type)
        instance.ostype_id = validated_data.get('ostype_id', instance.ostype_id)
        instance.telnet_status = validated_data.get('telnet_status', instance.telnet_status)
        instance.snmp_status = validated_data.get('snmp_status', instance.snmp_status)
        instance.save()
        return instance
