# Generated by Django 4.2.11 on 2024-05-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgazer', '0010_remove_device_ipv4_remove_device_ipv6_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='context',
            field=models.JSONField(null=True),
        ),
    ]
