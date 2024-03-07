from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModel
from mcfields import settings
from mcfields.base.storages import PublicMediaStorage


def public_storage():
    if settings.AWS_ACCESS_KEY_ID:
        return PublicMediaStorage()
    else:
        return FileSystemStorage()


class Servico(OrderedModel):
    title = models.CharField(max_length=64, verbose_name='Título')
    intro = models.TextField(max_length=512, verbose_name='Introdução')
    home_picture = models.ImageField(verbose_name='Foto da home page', storage=public_storage)
    content = CKEditor5Field(verbose_name='Conteúdo')
    slug = models.SlugField(max_length=64, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('servicos:detalhe_servico', args=(self.slug,))

    def get_edition_url(self):
        return reverse('servicos:edicao', args=(self.pk,))
