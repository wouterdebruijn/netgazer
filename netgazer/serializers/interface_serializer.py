from rest_framework.serializers import ModelSerializer
from netgazer.models import Interface


class InterfaceSerializer(ModelSerializer):
    class Meta:
        model = Interface
        fields = '__all__'
