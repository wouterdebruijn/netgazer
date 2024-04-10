from django.db import models
from .interface import Interface
from .neighbor import Neighbor
from django.urls import reverse


class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    os = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    interface_set: models.QuerySet[Interface]
    neighbor_set: models.QuerySet[Neighbor]

    run_id = models.UUIDField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('device-detail', kwargs={'pk': self.pk})

    def ipv4_addresses(self):
        return self.interface_set.filter(ipv4__isnull=False).values_list('ipv4', flat=True)

    class Meta:
        ordering = ['name']
        app_label = 'netgazer'
