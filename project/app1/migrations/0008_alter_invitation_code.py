# Generated by Django 5.0.6 on 2024-06-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_invitation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
