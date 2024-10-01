from rest_framework import generics, status
from rest_framework.response import Response

from payment.models import Subscription
from .models import WatchHistory, VideoModel
from .permition import IsOwner
from .serializer import VideoSerializer, WatchHistorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# List and Create Videos
class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(content_creator=self.request.user)

# Retrieve, Update, and Delete a Video
class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        video = self.get_object()
        user = request.user
        if not (video.content_creator == user or Subscription.objects.filter(user=user, video=video,is_active=True).exists()):
            return Response({"detail": "You need to subscribe to access this video."}, status=status.HTTP_403_FORBIDDEN)
        WatchHistory.objects.get_or_create(user=user, video=video)
        return response


# class WatchHistoryCreateView(generics.CreateAPIView):
#     queryset = WatchHistory.objects.all()
#     serializer_class = WatchHistorySerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         video = self.request.data.get('video')
#         serializer.save(user=user, video_id=video)
