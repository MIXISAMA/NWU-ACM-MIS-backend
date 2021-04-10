from rest_framework import serializers
from person.models import User, Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True)
    class Meta:
        model = User
        fields = ['stu_id', 'cf_id', 'nickname', 'need_peer', 'regions']
