from rest_framework import serializers
from backend.apolo.models import User, Entry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('name', 'mail')
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.mail = validated_data.get('mail', instance.mail)
        instance.save()
        return instance


class EntrySerializer(serializers.ModelSerializer):
    author = UserSerializer()

    # add extra fields
    # url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Entry
        fields = ('title', 'body', 'created_at', 'status', 'author')
        # fields = '__all__'
        # exclude = ('title',)
        # read_only_fields = ('status',)
        # depth = 1
