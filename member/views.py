from rest_framework import mixins, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from user.models import User
from member.models import Member
from member.serializers import MemberSerializer, MemberConciseSerializer
class IsCoach(permissions.BasePermission):
    """只允许教练访问"""
    def has_permission(self, request, view):
        return request.user.role == User.Role.COACH
class IsMember(permissions.BasePermission):
    """只允许协会队员访问"""
    def has_permission(self, request, view):
        return request.user.role == User.Role.MEMBER

class MemberAPIView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    """队员视图集"""
    permission_classes = (permissions.IsAuthenticated, IsMember|IsCoach)
    lookup_field = 'user__email'
    lookup_value_regex = '[^/]+'
    queryset = Member.objects.filter(user__is_banned=False).all()
    serializer_class = MemberSerializer

    # def update(self, request, *args, **kwargs):
    #     print(request.data)
    #     return super().update(request, *args, **kwargs)
    
    # def perform_update(self, serializer):
    #     print(serializer.validated_data)
    #     return super().perform_update(serializer)

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberConciseSerializer
        return super().get_serializer_class()
    
    def get_object(self):
        if self.kwargs[self.lookup_field] == 'self':
            self.kwargs[self.lookup_field] = self.request.user.email
        return super().get_object()
    
    # @action(('get',), False, 'self', 'self_profile',
    #         permission_classes=(permissions.IsAuthenticated, IsMember))
    # def get_self_profile(self, request):
    #     self.kwargs[self.lookup_field] = self.request.user.email
    #     return self.retrieve(request)

class MemberSelfAPIView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    """队员自身视图集"""
    permission_classes = (permissions.IsAuthenticated, IsMember)
    serializer_class = MemberSerializer

    def get_object(self):
        return Member.objects.get(user=self.request.user)
