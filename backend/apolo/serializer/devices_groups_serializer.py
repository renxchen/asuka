#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: action_policy_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import DevicesGroups


class DevicesGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevicesGroups
        fields = ('devicegroup_id', 'device', 'group', 'group_name')
