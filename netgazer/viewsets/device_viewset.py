from rest_framework.viewsets import ModelViewSet
from netgazer.models import Device, Interface, Neighbor
from netgazer.serializers import DeviceSerializer, InterfaceSerializer, NeighborSerializer
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import permissions


class RetrieveDeviceMixin(RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        interfaces = Interface.objects.filter(device=instance)
        neighbors = Neighbor.objects.filter(device=instance)

        interfaces = InterfaceSerializer(interfaces, many=True).data
        neighbors = NeighborSerializer(neighbors, many=True).data

        return Response(serializer.data | {'interfaces': interfaces, 'neighbors': neighbors})


class DeviceViewSet(ModelViewSet, RetrieveDeviceMixin):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAdminUser]
