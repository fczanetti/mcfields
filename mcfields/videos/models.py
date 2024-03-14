from django.db import models
from django.urls import reverse
from ordered_model.models import OrderedModel
from mcfields.base.models import Subject


class Video(OrderedModel):
    title = models.CharField(max_length=64, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='Assunto')
    platform_id = models.CharField(max_length=48, verbose_name='ID da plataforma')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Slug')
    post_date = models.DateField(auto_now_add=True, verbose_name='Data de postagem')
    edit_date = models.DateField(auto_now=True, verbose_name='Data de postagem')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos:detalhe_video', kwargs={'slug': self.slug, 'subject_slug': self.subject.slug})

    def get_edition_url(self):
        return reverse('videos:edicao', args=(self.pk,))
