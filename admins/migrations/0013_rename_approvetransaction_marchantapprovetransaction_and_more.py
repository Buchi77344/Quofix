# Generated by Django 5.0.1 on 2024-04-19 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0012_approvetransaction'),
        ('marchant', '0014_marchantprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApproveTransaction',
            new_name='MarchantApproveTransaction',
        ),
        migrations.RenameModel(
            old_name='PendingTransaction',
            new_name='MarchantPendingTransaction',
        ),
    ]
