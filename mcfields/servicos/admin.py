from django.contrib import admin
from mcfields.servicos.models import Servico


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['title', 'intro', 'slug', 'order']
    prepopulated_fields = {'slug': ['title']}
