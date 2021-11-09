from rest_framework import serializers
from .models import Sucursal


class ListarSucursalesSerializado(serializers.ModelSerializer):
    lat_lon = serializers.CharField(source='geo', read_only=True)

    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'lat_lon', 'activo', 'id']