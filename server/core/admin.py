from django.contrib import admin

from core.models import DownloadStatus


# Register your models here.
@admin.register(DownloadStatus)
class DownloadStatusAdmin(admin.ModelAdmin):
    list_display = [
        'youtube_id',
        'error',
        'download_path',
        'created_at'
    ]
