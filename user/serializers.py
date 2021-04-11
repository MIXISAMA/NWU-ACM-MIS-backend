from rest_framework import serializers

from user.models import User

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
