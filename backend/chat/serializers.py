from rest_framework import serializers

# from django.contrib.auth import get_user_model

from .models import ChatModel


# class UserGetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ["email", "full_name", "id"]
#         extra_kwargs = {"id": {"read_only": True}}


class ChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = "__all__"
