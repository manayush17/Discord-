# Generated by Django 5.0.6 on 2024-07-28 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_channel_channel_type_channel_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channel_type',
            field=models.CharField(choices=[('text', 'Text'), ('audio', 'audio'), ('video', 'Video')], default='text', max_length=10),
        ),
    ]
