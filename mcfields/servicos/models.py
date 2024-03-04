from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModel


class Servico(OrderedModel):
    title = models.CharField(max_length=64, verbose_name='Título')
    intro = models.CharField(max_length=512, verbose_name='Introdução')
    home_picture = models.ImageField(upload_to='servicos/', verbose_name='Foto da home page')
    content = CKEditor5Field(verbose_name='Conteúdo')
    slug = models.SlugField(max_length=64, verbose_name='Slug')

    def __str__(self):
        return self.title
