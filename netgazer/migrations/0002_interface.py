# Generated by Django 5.0.4 on 2024-04-08 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgazer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('ipv4', models.GenericIPAddressField(protocol='IPv4', unique=True)),
                ('ipv6', models.GenericIPAddressField(null=True, protocol='IPv6', unique=True)),
                ('mac', models.CharField(max_length=17, null=True, unique=True)),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='netgazer.device')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='netgazer.interface')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
