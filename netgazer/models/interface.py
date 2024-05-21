from django.db import models


class Interface(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    ipv4 = models.GenericIPAddressField(protocol='IPv4', null=True)
    ipv4_mask = models.PositiveSmallIntegerField(null=True)
    ipv6 = models.GenericIPAddressField(protocol='IPv6', null=True)
    ipv6_mask = models.PositiveSmallIntegerField(null=True)

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True)

    device = models.ForeignKey(
        'Device', on_delete=models.CASCADE)

    mac = models.CharField(max_length=17, unique=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    protocol = models.BooleanField(default=False)
    physical = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.ipv4}"

    class Meta:
        ordering = ['name']
        app_label = 'netgazer'
