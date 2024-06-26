# Generated by Django 5.0.3 on 2024-03-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('name', models.CharField(max_length=32, verbose_name='Nome')),
                ('email', models.EmailField(max_length=48, verbose_name='Email')),
                ('subject', models.CharField(max_length=128, verbose_name='Assunto')),
                ('message', models.TextField(verbose_name='Mensagem')),
                ('agree_with_policy', models.BooleanField()),
                ('send_date', models.DateField(auto_now_add=True, verbose_name='Data de envio')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
