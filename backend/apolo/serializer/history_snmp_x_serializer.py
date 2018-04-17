#!/usr/bin/env python
"""

@author: necwang
@contact: necwang@cisco.com
@file: history_snmp_x_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import HistorySnmpInt


class HistorySnmpXSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySnmpInt
        fields = '__all__'
