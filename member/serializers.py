from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer, UserConciseSerializer
from member.models import Achievement, Member, Team

class MemberConciseSerializer(serializers.ModelSerializer):
    user = UserConciseSerializer()
    class Meta:
        model = Member
        fields = (
            'user',
            'role',
            'realname',
            'stu_id',
        )
        read_only_fields = fields

class TeamSerializer(serializers.ModelSerializer):
    members = MemberConciseSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ('id', 'name_ch', 'name_en', 'members')
        read_only_fields = ('id', 'members')

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'level', 'detail')
        read_only_fields = fields

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    team = TeamSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    achievements = AchievementsSerializer(many=True, read_only=True)
    class Meta:
        model = Member
        fields = (
            'user',
            'role',
            'stu_id',
            'realname',
            'college',
            'department',
            'grade',
            'cf_id',
            'vj_id',
            'need_peer',
            'team',
            'tags',
            'achievements',
        )
        read_only_fields = (
            'role',
            'stu_id',
            'realname',
            'college',
            'department',
            'grade',
            'team',
            'tags',
            'achievements',
        )

    def update(self, instance: Member, validated_data: dict):
        user_data: dict = validated_data.pop('user', None)
        if user_data is not None:
            serializer = UserSerializer(instance.user, user_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return super().update(instance, validated_data)
