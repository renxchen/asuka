#!/usr/bin/env python

'''

@author: kimli
@contact: kimli@cisco.com
@file: policytree_serializer.py
@time: 2017/12/20 16:02
@desc:

'''
from rest_framework import serializers
from backend.apolo.models import CollPolicyRuleTree, CollPolicyCliRule


class CollPolicyRuleTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollPolicyRuleTree
        # fields = ('name', 'mail')
        fields = '__all__'

    def create(self, validated_data):
        return CollPolicyRuleTree.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class CollPolicyCliRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollPolicyCliRule
        fields = '__all__'

    def create(self, validated_data):
        return CollPolicyCliRule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.key_str = validated_data.get('key_str', instance.key_str)
        instance.mark_string = validated_data.get('mark_string', instance.mark_string)
        instance.split_char = validated_data.get('split_char', instance.split_char)
        instance.x_offset = validated_data.get('x_offset', instance.x_offset)
        instance.y_offset = validated_data.get('y_offset', instance.y_offset)
        instance.line_nums = validated_data.get('line_nums', instance.line_nums)
        instance.rule_type = validated_data.get('rule_type', instance.rule_type)
        instance.end_mark_string = validated_data.get('end_mark_string', instance.end_mark_string)
        instance.start_line_num = validated_data.get('start_line_num', instance.start_line_num)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.is_serial = validated_data.get('is_serial', instance.is_serial)
        instance.is_include = validated_data.get('is_include', instance.is_include)
        instance.command = validated_data.get('command', instance.command)
        instance.save()
        return instance
