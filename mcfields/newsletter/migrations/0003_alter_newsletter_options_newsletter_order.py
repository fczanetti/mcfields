# Generated by Django 5.0.3 on 2024-03-04 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_alter_newsletter_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='newsletter',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
    ]