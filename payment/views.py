from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription, VideoModel, Payment, PaymentHistory
from datetime import timedelta

from django.utils import timezone

from .serializer import SubscriptionSerializer


class SubscribeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, video_id):
        video = VideoModel.objects.get(id=video_id)
        user = request.user
        amount = request.data['amount']
        existing_subscription = Subscription.objects.filter(user=user, video=video, is_active=True).first()

        if existing_subscription:
            return Response({"detail": "You already have an active subscription for this video."},
                            status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=user,
            amount=amount,
            status='completed',
        )

        subscription = Subscription.objects.create(
            user=user,
            video=video,
            payment=payment,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            is_active=True,
        )

        # Create a payment history record
        PaymentHistory.objects.create(
            payment=payment,
            user=user,
            video=video,
            amount=payment.amount,
            status=payment.status,
        )

        return Response({
            "detail": "Subscription activated successfully.",
            "subscription_id": subscription.id,
            "payment_id": payment.id
        },
            status=status.HTTP_201_CREATED,
        )


class CancelSubscriptionView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, video_id):
        user = request.user
        try:
            subscription = Subscription.objects.get(user=user, video_id=video_id, is_active=True)
        except Subscription.DoesNotExist:
            return Response({"detail": "No active subscription found."}, status=status.HTTP_404_NOT_FOUND)

        subscription.is_active = False
        subscription.save()

        return Response({"detail": "Subscription canceled successfully."}, status=status.HTTP_200_OK)


class RenewSubscriptionView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, video_id):
        user = request.user

        try:
            subscription = Subscription.objects.get(user=user, video_id=video_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "No active subscription found."}, status=status.HTTP_404_NOT_FOUND)

        payment_amount = request.data['amount']
        payment = Payment.objects.create(
            user=user,
            amount=payment_amount,
            status='completed',
        )

        subscription.is_active = True
        subscription.end_date += timedelta(days=30)
        subscription.save()

        PaymentHistory.objects.create(
            payment=payment,
            user=user,
            video=subscription.video,
            amount=payment.amount,
            status=payment.status
        )

        return Response({"detail": "Subscription renewed successfully."}, status=status.HTTP_200_OK)