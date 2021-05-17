from django.db.models import fields
from rest_framework import serializers

from user.models import User, Verification

class UserConciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nickname', 'avatar')
        read_only_fields = fields

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'nickname',
            'avatar',
            'role',
            'college',
            'date_joined',
        ]
        read_only_fields = ['email', 'avatar', 'role', 'date_joined']

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'avatar']
        read_only_fields = ('email',)

class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['email', 'code']
        extra_kwargs = {'code': {'write_only': True}}

class EmailRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'code', 'nickname', 'password']
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
