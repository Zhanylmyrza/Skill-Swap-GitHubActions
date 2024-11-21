# from pyexpat import model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "full_name", "password")


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = User
        exclude = [
            "password",
            "is_active",
            "last_login",
            "user_permissions",
            "groups",
            "saved_persons",
        ]


class SingleProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, required=False)
    saved_persons = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = [
            "password",
            "is_active",
            "last_login",
            "user_permissions",
            "groups",
        ]
