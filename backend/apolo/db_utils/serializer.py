from rest_framework import serializers
from backend.apolo.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('name', 'mail')
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.token = validated_data.get('token', instance.token)
        instance.mail = validated_data.get('mail', instance.mail)
        instance.save()
        return instance
