# Generated by Django 5.0.1 on 2024-04-10 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0007_remove_pendingtransaction_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingtransaction',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
