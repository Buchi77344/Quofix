# Generated by Django 5.0.1 on 2024-04-08 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_ledger_balance_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='available_balance',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='ledger_balance',
            name='slug',
        ),
    ]
