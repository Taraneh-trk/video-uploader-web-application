from rest_framework import serializers
from .models import VideoModel, WatchHistory, Comment, Rating, VideoStatus


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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class VideoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoStatus
        fields = '__all__'
        read_only_fields = ['video']