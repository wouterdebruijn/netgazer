from rest_framework.viewsets import ModelViewSet
from netgazer.models import Interface
from netgazer.serializers import InterfaceSerializer
from rest_framework import permissions


class InterfaceViewSet(ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    permission_classes = [permissions.IsAdminUser]
