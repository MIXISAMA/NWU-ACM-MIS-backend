from rest_framework import permissions

from user.models import User
from member.models import Member, Team

class IsCoachAndReadOnly(permissions.BasePermission):
    """只允许教练访问"""
    def has_permission(self, request, view):
        read_only: bool = request.method in permissions.SAFE_METHODS
        is_coach: bool = request.user.role == User.Role.COACH
        return read_only and is_coach

class IsMember(permissions.BasePermission):
    """只允许协会队员访问"""
    def has_permission(self, request, view):
        return request.user.role == User.Role.MEMBER

class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Member):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user.member

class IsSelfTeamOrReadOnly(permissions.BasePermission):
    """只允许操作自己的Team"""
    def has_object_permission(self, request, view, obj: Team):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user.member.team