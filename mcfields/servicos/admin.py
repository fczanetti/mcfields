from django.contrib import admin
from mcfields.servicos.models import Service


@admin.register(Service)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order']
    prepopulated_fields = {'slug': ['title']}
