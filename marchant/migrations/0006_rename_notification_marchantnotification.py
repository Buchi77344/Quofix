# Generated by Django 5.0.1 on 2024-04-08 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marchant', '0005_notification'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='MarchantNotification',
        ),
    ]
