from rest_framework import serializers
from .models import VideoModel, WatchHistory


class VideoSerializer(serializers.ModelSerializer):
    content_creator = serializers.ReadOnlyField(source='content_creator.username')

    class Meta:
        model = VideoModel
        fields = ['id', 'title', 'description', 'video_url', 'content_creator', 'upload_date']

class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchHistory
        fields = '__all__'
        read_only_fields = ['user', 'watch_date']