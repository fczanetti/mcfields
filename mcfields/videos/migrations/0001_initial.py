# Generated by Django 5.0.3 on 2024-03-14 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0002_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=64, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('platform_id', models.CharField(max_length=48, verbose_name='ID da plataforma')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
                ('post_date', models.DateField(auto_now_add=True, verbose_name='Data de postagem')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Data de postagem')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.subject',
                                              verbose_name='Assunto')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
