from rest_framework.viewsets import ModelViewSet
from netgazer.models import Device
from netgazer.serializers import DeviceSerializer
from rest_framework import permissions


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAdminUser]
