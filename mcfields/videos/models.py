from django.db import models
from ordered_model.models import OrderedModel
from mcfields.base.models import Assunto


class Video(OrderedModel):
    title = models.CharField(max_length=64, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    assunto = models.ForeignKey(Assunto, on_delete=models.PROTECT, verbose_name='Assunto')
    platform_id = models.CharField(max_length=48, verbose_name='ID da plataforma')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Slug')
    post_date = models.DateField(auto_now_add=True, verbose_name='Data de postagem')
    edit_date = models.DateField(auto_now=True, verbose_name='Data de postagem')

    def __str__(self):
        return self.title
