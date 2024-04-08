from rest_framework.viewsets import ModelViewSet
from netgazer.models import Neighbor
from netgazer.serializers import NeighborSerializer
from rest_framework import permissions


class NeighborViewSet(ModelViewSet):
    queryset = Neighbor.objects.all()
    serializer_class = NeighborSerializer
    permission_classes = [permissions.IsAdminUser]
