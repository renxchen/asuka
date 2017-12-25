#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: policytree_serializer.py
@time: 2017/12/20 16:02
@desc:

'''
from rest_framework import serializers
from backend.apolo.models import CollPolicyRuleTree


class CollPolicyRuleTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollPolicyRuleTree
        # fields = ('name', 'mail')
        fields = '__all__'

    def create(self, validated_data):
        return CollPolicyRuleTree.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
