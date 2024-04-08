# Generated by Django 5.0.4 on 2024-04-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgazer', '0003_alter_interface_device_alter_interface_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ipv4',
            field=models.GenericIPAddressField(null=True, protocol='IPv4'),
        ),
        migrations.AlterField(
            model_name='device',
            name='ipv6',
            field=models.GenericIPAddressField(null=True, protocol='IPv6'),
        ),
    ]
