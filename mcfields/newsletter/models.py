from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModel


class Newsletter(OrderedModel):
    title = models.CharField(max_length=64, verbose_name='Título')
    intro = models.TextField(max_length=512, verbose_name='Introdução')
    content = CKEditor5Field(verbose_name='Conteúdo')
    pub_date = models.DateField(auto_now_add=True, verbose_name='Data de publicação')
    edit_date = models.DateField(auto_now=True, verbose_name='Data de edição')
    author = models.CharField(max_length=32, verbose_name='Autor')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsletter:detalhe_newsletter', args=(self.slug,))

    def get_edition_url(self):
        return reverse('newsletter:edicao', args=(self.pk,))

    def get_removal_url(self):
        return reverse('newsletter:remocao', args=(self.pk,))
