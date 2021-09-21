from rest_framework import serializers
from propietarios.models import Propietarios


class ListarSerializado(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(source='nombreCompleto', read_only=True)
    la_comuna = serializers.CharField(source='comuna_text', read_only=True)

    class Meta:
        model = Propietarios
        fields = ['id', 'rut', 'nombre_completo', 'direccion', 'la_comuna', 'telefono', 'activo', 'nombre', 'email']