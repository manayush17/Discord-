# Generated by Django 5.0.6 on 2024-06-27 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_server_moderators_alter_message_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='moderators',
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('moderator', 'Moderator')], default='member', max_length=10),
        ),
    ]
