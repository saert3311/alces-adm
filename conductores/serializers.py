from rest_framework import serializers
from conductores.models import Conductor


class ListarSerializado(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(source='nombreCompleto', read_only=True)
    la_comuna = serializers.CharField(source='comuna_text', read_only=True)
    la_foto = serializers.CharField(source='foto_url', read_only=True)

    class Meta:
        model = Conductor
        fields = ['id', 'rut', 'nombre_completo', 'direccion', 'la_comuna', 'telefono', 'venc_licencia', 'la_foto', 'licencia', 'email', 'nombre']