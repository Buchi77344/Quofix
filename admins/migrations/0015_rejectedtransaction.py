# Generated by Django 5.0.1 on 2024-04-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0014_remove_marchantapprovetransaction_pending_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RejectedTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('action', models.CharField(max_length=10)),
                ('message', models.TextField(null=True)),
                ('is_rejected', models.BooleanField(default=True)),
            ],
        ),
    ]
