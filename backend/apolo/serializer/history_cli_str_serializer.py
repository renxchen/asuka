#!/usr/bin/env python
"""

@author: necwang
@contact: necwang@cisco.com
@file: history_cli_str_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import HistoryCliStr


class HistoryCliStrSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryCliStr
        fields = '__all__'
