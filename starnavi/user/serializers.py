from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        max_length=128, write_only=True, style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        max_length=128, write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'nickname',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')
        validate_password(password1, self.instance)
        if password1 and password2 and password1 != password2:
            raise ValidationError('password mismatch')
        user = User.objects.create_user(password = password1, **validated_data)
        return user


class UserLastLoginTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'nickname',
            'first_name',
            'last_name',
            'last_login',
        ]
