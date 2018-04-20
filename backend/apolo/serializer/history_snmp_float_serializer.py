#!/usr/bin/env python
"""

@author: necwang
@contact: necwang@cisco.com
@file: history_snmp_float_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import HistorySnmpFloat


class HistorySnmpFloatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySnmpFloat
        fields = '__all__'
