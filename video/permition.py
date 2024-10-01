from rest_framework.permissions import BasePermission
from .models import VideoModel

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        return obj.content_creator == request.user
