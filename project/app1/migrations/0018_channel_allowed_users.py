# Generated by Django 5.0.6 on 2024-08-04 08:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_alter_channel_channel_type_alter_channel_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='allowed_channels', to=settings.AUTH_USER_MODEL),
        ),
    ]
