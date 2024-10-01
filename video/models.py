from django.db import models

from accounts.models import CustomUser


class VideoModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(max_length=500)
    content_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WatchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    watch_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f'{self.user} watched {self.video} in {self.watch_date} . '