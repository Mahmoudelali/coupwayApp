from djoser.serializers import TokenCreateSerializer
from rest_registration.api.serializers import DefaultRegisterUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User


class CustomTokenCreateSerializer(TokenCreateSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()

    def create(self, validated_data):
        user = self.user
        token, _ = self.token_model.objects.get_or_create(user=user)
        return {
            "auth_token": token.key,
            "id": user.id,
            "username": user.username,
        }


class CustomRegisterSerializer(DefaultRegisterUserSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        fields = "__all__"
