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


class MobileVerificationSerializer(serializers.ModelSerializer):
    '''
    Serializer for mobile number verification.
    '''
    class Meta:
        model = User
        fields = ('mobile', 'mobile_otp', 'otp_generated_at')