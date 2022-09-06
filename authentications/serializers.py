from dataclasses import fields
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    '''
    Serializer for user registration.
    '''
    class Meta:
        model = User
        fields = [
            'email', 'mobile', 'first_name', 'last_name', 'country', 'mobile_otp',
            ]

    def create(self, validated_data):
        '''
        Method to create user.
        '''
        user = User(**validated_data)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('mobile', 'mobile_otp', 'email', 'token')

        read_only_fields = ['token']


class GenLoginOTPSerializer(serializers.Serializer):

    mobile = serializers.CharField()
    # email = serializers.EmailField(required=False)