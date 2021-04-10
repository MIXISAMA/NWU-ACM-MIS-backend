from rest_framework import serializers
from person.models import User, Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']
        read_only = ['id']

class UserSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['stu_id', 'cf_id', 'nickname', 'need_peer', 'regions']
        read_only = ['stu_id', 'regions']
