from rest_framework import serializers

from user.models import User, Verification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'stu_id',
            'email',
            'is_verified',
            'cf_id',
            'nickname',
            'realname',
            'need_peer',
            'avatar',
        ]
        read_only = ['stu_id', 'email', 'is_verified', 'realname']


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
