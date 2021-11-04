from rest_framework import serializers
from .models import Despacho, Servicio


class UltimosDespachos(serializers.ModelSerializer):
    #nombre_completo = serializers.CharField(source='nombreCompleto', read_only=True)
    #la_comuna = serializers.CharField(source='comuna_text', read_only=True)

    class Meta:
        model = Despacho
        fields = ['__all__']

class ListarRecorridoSerial(serializers.ModelSerializer):
    distancia_kms = serializers.CharField(source='kms', read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'distancia_kms', 'es_vigente', 'valor_planilla', 'nombre']