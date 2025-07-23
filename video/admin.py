from django.contrib import admin

from video.models import VideoModel, WatchHistory

admin.site.register(VideoModel)
admin.site.register(WatchHistory)
