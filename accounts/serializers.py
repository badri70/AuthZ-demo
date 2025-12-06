from rest_framework import serializers
from django.contrib.auth import password_validation


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    password_1 = serializers.CharField(max_length=128, write_only=True)
    password_2 = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)


class ProfileUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class ProfileDeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()