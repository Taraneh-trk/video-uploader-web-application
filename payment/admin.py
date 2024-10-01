from django.contrib import admin

from payment.models import Subscription, Payment, PaymentHistory

admin.site.register(Subscription)
admin.site.register(Payment)
admin.site.register(PaymentHistory)
