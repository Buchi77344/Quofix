# Generated by Django 5.0.1 on 2024-04-23 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_kyc_user_alter_kyc_gender_alter_kyc_nin_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kyc',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.userprofile'),
        ),
    ]
