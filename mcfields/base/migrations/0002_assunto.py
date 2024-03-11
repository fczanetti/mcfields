# Generated by Django 5.0.3 on 2024-03-11 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assunto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=64, verbose_name='Título')),
                ('description', models.TextField(max_length=256, verbose_name='Descrição')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
