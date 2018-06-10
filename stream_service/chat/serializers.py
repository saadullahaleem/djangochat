from rest_framework import serializers
from .models import User, Message


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('message', 'created',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'alias')
