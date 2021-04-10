from rest_framework import serializers
from team.models import Team, Contest, TeamContest, Reward

class TeamSerializer(serializers.ModelSerializer):
    #users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['id', 'name', 'disable'] # 缺user
        read_only_fields = ['id']


class ContestSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    class Meta:
        model = Contest
        fields = ['id', 'teams', 'name', 'start_time', 'contest_type', 'contest_level']
        read_only_fields = ['id']


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'team_contest', 'record']
        read_only_fields = ['id']
