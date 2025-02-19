# Generated by Django 5.0.1 on 2024-04-23 09:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_rename_eur_wallet_eurwallet_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='kyc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Gender', models.CharField(choices=[('male', 'Male'), ('famale', 'Female')], max_length=20)),
                ('DOB', models.DateField()),
                ('email', models.EmailField(max_length=254, null=True)),
                ('adress', models.CharField(max_length=250, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('photo', models.FileField(upload_to='images/')),
                ('nin', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid NIN', message='NIN must contain only digits', regex='^[0-9]*$')])),
                ('nin_photo', models.FileField(upload_to='images/')),
                ('information', models.BooleanField(default=False)),
            ],
        ),
    ]
