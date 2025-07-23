from django.urls import path

from accounts.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('signup/',RegisterView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
]