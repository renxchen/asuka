from rest_framework import serializers
from backend.apolo.models import CollPolicy, CollPolicyGroups, Ostype, PolicysGroups


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


class CollPolicyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollPolicy
        fields = ('name', 'policy_type',)


class CollPolicyGroupSerializer(serializers.ModelSerializer):
    # ostype_name = serializers.RelatedField(source='ostype', read_only=True)
    # ostype_name = serializers.ReadOnlyField()
    class Meta:
        model = CollPolicyGroups
        fields = ('policy_group_id', 'name', 'desc', 'ostype', 'ostype_name', 'ostype_ostypeid',)
        # fields = '__all__'

    def create(self, validated_data):
        return CollPolicyGroups.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.ostype = validated_data.get('ostype', instance.ostype)
        instance.save()
        return instance


class PolicyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicysGroups
        fields = ('policys_groups_id', 'exec_interval', 'status', 'history', 'policy', 'policy_group')

    def create(self, validated_data):
        return PolicysGroups.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.policys_groups_id = validated_data.get('policys_groups_id', instance.policys_groups_id)
        instance.desc = validated_data.get('exec_interval', instance.exec_interval)
        instance.status = validated_data.get('status', instance.status)
        instance.history = validated_data.get('history', instance.history)
        instance.policy = validated_data.get('policy', instance.policy)
        instance.policy_group = validated_data.get('policy_group', instance.policy_group)
        instance.save()
        return instance


class OstypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ostype
        fields = ('ostypeid', 'name',)

        # def create(self, validated_data):
        #     return Ostype.objects.create(**validated_data)
        #
        # def update(self, instance, validated_data):
        #     instance.name = validated_data.get('name', instance.name)
        #     instance.log_fail_judges = validated_data.get('log_fail_judges', instance.log_fail_judges)
        #     instance.status = validated_data.get('status', instance.status)
        #     instance.snmp_timeout = validated_data.get('snmp_timeout', instance.snmp_timeout)
        #     instance.telnet_timeout = validated_data.get('telnet_timeout', instance.telnet_timeout)
        #     instance.telnet_prompt = validated_data.get('telnet_prompt', instance.telnet_prompt)
        #     instance.start_default_commands = validated_data.get('start_default_commands', instance.start_default_commands)
        #     instance.end_default_commands = validated_data.get('end_default_commands', instance.end_default_commands)
        #     instance.desc = validated_data.get('desc', instance.desc)
        #     instance.save()
        #     return instance
