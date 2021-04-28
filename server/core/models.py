from django.db import models

# Create your models here.
class DownloadStatus(models.Model):
    youtube_id = models.CharField(
        max_length=12
    )

    error = models.TextField(
        null=True,
        blank=True
    )

    download_path = models.CharField(
        max_length=250
    )

    subset = models.CharField(
        max_length=12,
        null=True,
        blank=True
    )

    url = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    label = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
