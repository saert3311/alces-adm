from rest_framework import serializers
from .models import Despacho, Servicio, Planilla


class UltimosDespachosSerial(serializers.ModelSerializer):
    recorrido_despacho = serializers.CharField(source='detalle', read_only=True)
    la_planilla = serializers.CharField(source='control_planilla', read_only=True)

    class Meta:
        model = Despacho
        fields = ['id', 'nro_vehiculo', 'hora_salida_ss', 'recorrido_despacho', 'la_planilla']

class ListarRecorridoSerial(serializers.ModelSerializer):
    distancia_kms = serializers.CharField(source='kms', read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'distancia_kms', 'es_vigente', 'valor_planilla', 'nombre']

class ListarPlanillasPendientes(serializers.ModelSerializer):
    nro_bus = serializers.CharField(source='nro_vehiculo', read_only=True)
    servicio_text = serializers.CharField(source='servicio_desc', read_only=True)
    valor = serializers.CharField(source='valor_planilla', read_only=True)

    class Meta:
        model = Planilla
        fields = ['nro_bus', 'fecha_planilla', 'nro_control', 'id', 'servicio_text', 'valor']