from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from person.serializers import UserSerializer, RegionSerializer
from person.models import User, Region


class UserList(APIView):
    """用户"""
    def post(self, request, format=None):
        """增加"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        """查询"""
        if pk is None:
            if request.data.__contains__('region'): #根据领域查询有哪些用户
                users = User.objects.filter(regions__pk__contains = request.data['region'])
            else:
                users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        else:
            user = get_object_or_404(User, pk)
            serializer = UserSerializer(user)
           
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """修改"""
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """删除"""
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegionList(APIView):
    """板块"""
    def get(self, request, pk=None, format=None):
        """查询"""
        if pk is None:
            if request.data.__contains__('user'): #根据用户查询有哪些领域
                regions = Region.objects.filter(users__pk__contains = request.data['user'])
            else:
                regions = Region.objects.all()
            serializer = RegionSerializer(regions, many=True)
        else:
            region = get_object_or_404(Region, pk=pk)
            serializer = RegionSerializer(region)

        return Response(serializer.data)

