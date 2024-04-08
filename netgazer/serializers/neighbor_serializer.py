from rest_framework.serializers import ModelSerializer
from netgazer.models import Neighbor


class NeighborSerializer(ModelSerializer):
    class Meta:
        model = Neighbor
        fields = '__all__'
