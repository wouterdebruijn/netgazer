from django.db import models


class Neighbor(models.Model):
    name = models.CharField(max_length=255)
    ipv4 = models.GenericIPAddressField(null=True)
    ipv6 = models.GenericIPAddressField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    neighbor_device = models.ForeignKey(
        'Device', on_delete=models.CASCADE, related_name='neighbor_device', null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'netgazer'
