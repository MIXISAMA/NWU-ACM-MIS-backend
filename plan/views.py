from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from plan.models import Announcement
from plan.serializers import (
    AnnouncementSerializer, AnnouncementSimpleSerializer
)

class AnnouncementView(APIView):
    """公告"""
    permission_classes = []
    def get(self, request, id=None):
        """查询"""
        if id is None:
            annos = Announcement.objects.all()
            serializer = AnnouncementSimpleSerializer(annos, many=True)
        else:
            anno = get_object_or_404(Announcement, id=id)
            serializer = AnnouncementSerializer(anno)
        return Response(serializer.data, status=status.HTTP_200_OK)
