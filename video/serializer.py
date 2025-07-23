from rest_framework import serializers
from .models import VideoModel, WatchHistory, Comment, Rating


# class VideoSerializer(serializers.ModelSerializer):
#     content_creator = serializers.ReadOnlyField(source='content_creator.username')
#
#     class Meta:
#         model = VideoModel
#         fields = ['id', 'title', 'description', 'video_url', 'content_creator', 'upload_date']

class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchHistory
        fields = '__all__'
        read_only_fields = ['user', 'watch_date']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['id', 'user', 'rate', 'created_at', 'updated_at']

class VideoSerializer(serializers.ModelSerializer):
    content_creator = serializers.ReadOnlyField(source='content_creator.username')
    view_count = serializers.IntegerField(read_only=True)  # This is already in your model
    comments = CommentSerializer(many=True, read_only=True)  # Nested serializer for comments
    ratings = RatingSerializer(many=True, read_only=True)    # Nested serializer for ratings
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = VideoModel
        fields = ['id', 'title', 'description', 'video_url', 'content_creator', 'upload_date', 'view_count', 'comments', 'ratings', 'average_rating']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum([rating.rate for rating in ratings]) / ratings.count(), 2)
        return 0

# class VideoStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VideoStatus
#         fields = '__all__'
#         read_only_fields = ['video']