from django.urls import path

from payment.views import SubscribeView, CancelSubscriptionView, RenewSubscriptionView
from .views import VideoListCreateAPIView, VideoRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('videos/', VideoListCreateAPIView.as_view(), name='video_list_create'),
    path('videos/<int:pk>/', VideoRetrieveUpdateDestroyAPIView.as_view(), name='video_detail_update_delete'),
    path('videos/<int:video_id>/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('videos/<int:video_id>/cancel_subscription/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
    path('videos/<int:video_id>/renew_subscription/', RenewSubscriptionView.as_view(), name='renew_subscription'),
]
