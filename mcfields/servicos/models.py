from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModel


class Service(OrderedModel):
    title = models.CharField(max_length=64, verbose_name='Título')
    intro = models.TextField(max_length=512, verbose_name='Introdução')
    home_picture = models.ImageField(verbose_name='Foto da home page', upload_to='service_photos')
    content = CKEditor5Field(verbose_name='Conteúdo')
    slug = models.SlugField(max_length=64, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('servicos:detalhe_servico', args=(self.slug,))

    def get_edition_url(self):
        return reverse('servicos:edicao', args=(self.pk,))

    def get_removal_url(self):
        return reverse('servicos:remocao', args=(self.pk,))
