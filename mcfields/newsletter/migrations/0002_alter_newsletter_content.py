# Generated by Django 5.0.2 on 2024-02-25 16:03

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Conteúdo'),
        ),
    ]
