from rest_framework import mixins, permissions, status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view, permission_classes

from util.rest import detail
from member.models import Member, Tag, Team
from member.serializers import (
    MemberSerializer, MemberConciseSerializer, TeamSerializer
)
from member.permissions import (
    IsMember, IsCoachAndReadOnly, IsSelfOrReadOnly, IsSelfTeamOrReadOnly
)

class MemberAPIView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    """队员视图集"""
    permission_classes = (
        permissions.IsAuthenticated,
        IsMember&IsSelfOrReadOnly | IsCoachAndReadOnly
    )
    lookup_field = 'user__email'
    lookup_value_regex = '[^/]+'
    queryset = Member.objects.filter(user__is_banned=False).all()
    serializer_class = MemberSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberConciseSerializer
        return super().get_serializer_class()
    
    def get_object(self):
        if self.kwargs[self.lookup_field] == 'self':
            self.kwargs[self.lookup_field] = self.request.user.email
        return super().get_object()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsMember])
def join_team(request, id):
    """加入队伍"""
    member: Member = request.user.member
    if member.team is not None:
        return Response(detail('已经在一个队伍里面了'), status.HTTP_403_FORBIDDEN)
    member.team = get_object_or_404(Team, id=id)
    member.save(update_fields=['team'])
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsMember])
def leave_team(request, email):
    """请离当前队伍中某队员"""
    team: Team = request.user.member.team
    if team is None:
        return Response(detail('未加入任何队伍'), status.HTTP_403_FORBIDDEN)
    if email == 'self':
        member: Member = request.user.member
    else:
        member = get_object_or_404(Member, user__email=email)
    if member not in team.members.all():
        return Response(detail('队伍中无此人'), status.HTTP_403_FORBIDDEN)
    member.team = None
    member.save(update_fields=['team'])
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated, IsMember])
def tag(request, name):
    """添加/删除自己的标签"""
    member: Member = request.user.member
    if request.method == 'POST':
        tag, created = Tag.objects.get_or_create(name=name)
        tag.members.add(member)
    elif request.method == 'DELETE':
        tag = get_object_or_404(Tag, name=name)
        tag.members.remove(member)
    return Response(status=status.HTTP_204_NO_CONTENT)

class TeamAPIView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    """队伍视图集"""
    permission_classes = (
        permissions.IsAuthenticated,
        IsMember&IsSelfTeamOrReadOnly | IsCoachAndReadOnly,
    )
    lookup_field = 'id'
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_object(self):
        if self.kwargs[self.lookup_field] == '-1':
            team = self.request.user.member.team
            if team is None:
                raise Http404('未加入任何队伍')
            self.kwargs[self.lookup_field] = team.id
        return super().get_object()

    def create(self, request, *args, **kwargs):
        """创建并加入"""
        member: Member = request.user.member
        if member.team is not None:
            return Response(detail('已经在一个队伍里面了'), status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        team = Team.objects.get(id=serializer.data['id'])
        member.team = team
        member.save(update_fields=['team'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
