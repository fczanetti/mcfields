# Generated by Django 5.0.3 on 2024-03-06 20:07

import mcfields.servicos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0002_alter_servico_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='home_picture',
            field=models.ImageField(storage=mcfields.servicos.models.public_storage, upload_to='',
                                    verbose_name='Foto da home page'),
        ),
    ]
