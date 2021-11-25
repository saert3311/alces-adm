from rest_framework import serializers
from buses.models import Vehiculo


class ListarSerializado(serializers.ModelSerializer):
    veh_completo = serializers.CharField(source='get_descripcion', read_only=True)
    la_foto = serializers.CharField(source='get_foto', read_only=True)
    terminal_salida = serializers.CharField(source='t_salida_text', read_only=True)

    class Meta:
        model = Vehiculo
        fields = ['id', 'nro', 'patente', 'veh_completo', 'ano', 'ven_revision', 'terminal_salida', 'la_foto']