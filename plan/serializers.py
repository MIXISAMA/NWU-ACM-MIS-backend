from rest_framework import serializers

from plan.models import Announcement

class AnnouncementSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'created_date', 'changed_date')
        read_only = ('id',)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'created_date', 'changed_date')
        read_only = ('id',)
