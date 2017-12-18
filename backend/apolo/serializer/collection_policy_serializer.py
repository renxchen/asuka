from rest_framework import serializers
from backend.apolo.models import User
from backend.apolo.models import CollPolicy


class CollPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollPolicy
        # fields = ('name', 'mail')
        fields = '__all__'

    def create(self, validated_data):
        return CollPolicy.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cli_command = validated_data.get('cli_command', instance.cli_command)
        instance.cli_command_result = validated_data.get('cli_command_result', instance.cli_command_result)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.policy_type = validated_data.get('policy_type', instance.policy_type)
        instance.snmp_oid = validated_data.get('snmp_oid', instance.snmp_oid)
        instance.history = validated_data.get('history', instance.history)
        instance.ostype = validated_data.get('ostype', instance.ostype)
        instance.save()
        return instance
