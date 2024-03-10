# Generated by Django 5.0.3 on 2024-03-10 16:19

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=64, verbose_name='Título')),
                ('intro', models.TextField(max_length=512, verbose_name='Introdução')),
                ('home_picture', models.ImageField(upload_to='service_photos', verbose_name='Foto da home page')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Conteúdo')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
