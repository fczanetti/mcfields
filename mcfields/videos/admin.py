from django.contrib import admin
from mcfields.base.models import Assunto
from mcfields.videos.models import Video


@admin.register(Assunto)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'assunto', 'platform_id', 'slug', 'post_date', 'edit_date']
    prepopulated_fields = {'slug': ['title']}
