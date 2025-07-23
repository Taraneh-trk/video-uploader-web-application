from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from payment.models import Subscription
from .models import WatchHistory, VideoModel, Comment, Rating
from .permition import IsOwner, IsOwnerComment_Rating
from .serializer import VideoSerializer, WatchHistorySerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(content_creator=self.request.user)

class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        user = request.user
        subscription = None

        try:
            subscription = Subscription.objects.get(user=user, video=video)
            if timezone.is_naive(subscription.end_date):
                subscription.end_date = timezone.make_aware(subscription.end_date)

            if subscription.end_date < timezone.now():
                subscription.is_active = False
                subscription.save()
            print(subscription)

        except Subscription.DoesNotExist:
            if video.content_creator != user:
                return Response({"detail": "You need to subscribe to access this video."},
                                status=status.HTTP_403_FORBIDDEN)

        if subscription and not subscription.is_active and video.content_creator != user:
            return Response({"detail": "Your subscription has expired. Please renew to access this video."},
                            status=status.HTTP_403_FORBIDDEN)

        if user.is_authenticated:
            WatchHistory.objects.get_or_create(user=user, video=video)

        video.view_count += 1
        video.save()

        return super().retrieve(request, *args, **kwargs)



class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        video_id = self.kwargs.get('video_id')
        return Comment.objects.filter(video_id=video_id)

    def perform_create(self, serializer):
        video_id = self.kwargs.get('video_id')
        serializer.save(user=self.request.user, video_id=video_id)

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerComment_Rating]


class RatingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        video_id = self.kwargs.get('video_id')
        return Rating.objects.filter(video_id=video_id)

    def perform_create(self, serializer):
        video_id = self.kwargs.get('video_id')
        serializer.save(user=self.request.user, video_id=video_id)

class RatingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerComment_Rating]







# class WatchHistoryCreateView(generics.CreateAPIView):
#     queryset = WatchHistory.objects.all()
#     serializer_class = WatchHistorySerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         video = self.request.data.get('video')
#         serializer.save(user=user, video_id=video)


