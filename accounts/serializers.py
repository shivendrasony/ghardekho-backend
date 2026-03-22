from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model  = User
        fields = ['name', 'email', 'phone', 'password', 'password2', 'role', 'agency', 'rera_number']

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('Your account has been deactivated.')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = [
            'id', 'name', 'email', 'phone', 'role', 'city',
            'avatar', 'agency', 'rera_number', 'experience',
            'is_verified', 'date_joined',
        ]
        read_only_fields = ['id', 'is_verified', 'date_joined']


class UserPublicSerializer(serializers.ModelSerializer):
    """Public profile — used on agent profile pages"""
    class Meta:
        model  = User
        fields = ['id', 'name', 'role', 'city', 'avatar', 'agency', 'rera_number', 'experience', 'is_verified']


class TokenSerializer(serializers.Serializer):
    """Returns tokens + full user data"""
    access  = serializers.CharField()
    refresh = serializers.CharField()
    user    = UserSerializer()

    @classmethod
    def get_tokens(cls, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
            'user':    UserSerializer(user).data,
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value
