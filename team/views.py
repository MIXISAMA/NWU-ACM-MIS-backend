from django.shortcuts import render
from django.db.models import ProtectedError
from team.serializers import TeamSerializer
from team.serializers import ContestSerializer
from team.serializers import RewardSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from team.models import Team, Contest, TeamContest, Reward
from django.shortcuts import get_object_or_404
# Create your views here.

class TeamDetail(APIView):
    """队伍View"""

    def get(self, request, pk=None, format=None):
        """查询队伍"""
        if pk is None:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
        else:
            team = get_object_or_404(Team, pk=pk)
            serializer = TeamSerializer(team)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """修改队伍"""
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk=None, format=None):
        """增加队伍"""
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """删除队伍"""
        team = get_object_or_404(Team, pk=pk)
        try:
            team.delete()
        except ProtectedError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class ContestDetail(APIView):
    """比赛view"""
    def get(self, request, pk=None, format=None):
        """"查询比赛"""
        if pk is None:
            contests = Contest.objects.all()
            serializer = ContestSerializer(contests, many=True)
        else :
            contest = get_object_or_404(Contest, pk=pk)
            serializer = ContestSerializer(contest)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """修改比赛"""
        contest = get_object_or_404(Contest,pk=pk)
        serializer = ContestSerializer(contest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk=None, format=None):
        """增加比赛"""
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """删除比赛"""
        contest = get_object_or_404(Contest,pk=pk)
        contest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RewardDetail(APIView):
    """获奖view"""
    def get(self, request, pk=None, format=None):
        """查询奖项"""
        if pk is None:
            rewards = Reward.objects.all()
            serializer = RewardSerializer(rewards, many=True)
        else:
            reward = get_object_or_404(Reward, pk=pk)
            serializer = RewardSerializer(reward)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """修改奖项"""
        reward = get_object_or_404(Reward, pk=pk)
        serializer = ContestSerializer(reward, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk=None, format=None):
        """增加奖项"""
        serializer = RewardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """删除奖项"""
        reward = get_object_or_404(Reward, pk=pk)
        reward.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)