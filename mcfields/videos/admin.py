from django.contrib import admin
from mcfields.videos.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'platform_id', 'slug', 'post_date', 'edit_date']
    prepopulated_fields = {'slug': ['title']}
