from rest_framework.viewsets import ModelViewSet
from netgazer.models import Device
from netgazer.serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
