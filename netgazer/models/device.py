from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    ipv4 = models.GenericIPAddressField(protocol='IPv4', unique=True)
    ipv6 = models.GenericIPAddressField(
        protocol='IPv6', unique=True, null=True)

    mac = models.CharField(max_length=17, unique=True, null=True)
    os = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'netgazer'
