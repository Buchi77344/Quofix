# Generated by Django 5.0.1 on 2024-04-18 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_rename_timebool_usertimestamp_time_bool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertimestamp',
            name='timestamp',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
