#!/usr/bin/env python
"""

@author: necwang
@contact: necwang@cisco.com
@file: history_snmp_str_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import HistorySnmpStr


class HistorySnmpStrSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySnmpStr
        fields = '__all__'
