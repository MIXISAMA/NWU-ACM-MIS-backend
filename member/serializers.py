from rest_framework import serializers

from user.models import User

from member.models import Member

# class UserSerializer(serializers.ModelSerializer):
#     regions = RegionSerializer(many=True, read_only=True)
#     class Meta:
#         model = User
#         fields = ['stu_id', 'cf_id', 'nickname', 'need_peer', 'regions']
#         read_only = ['stu_id', 'regions']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', '']