#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: action_policy_serializer.py
@time: 2018/1/15 14:22
@desc:

"""
from rest_framework import serializers
from backend.apolo.models import HistoryCliFloat


class HistoryXSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryCliFloat
        fields = '__all__'
