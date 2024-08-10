# 0007_alter_invitation_code.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_remove_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(max_length=255, unique=True),  # Added max_length
        ),
    ]
