from django.contrib import admin
from mcfields.newsletter.models import Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'intro', 'pub_date', 'edit_date', 'author', 'slug']
    prepopulated_fields = {'slug': ['title']}
