from rest_framework import serializers
from .models import Despacho, Servicio, Planilla


class UltimosDespachosSerial(serializers.ModelSerializer):
    recorrido_despacho = serializers.CharField(source='detalle', read_only=True)
    la_planilla = serializers.CharField(source='control_planilla', read_only=True)

    class Meta:
        model = Despacho
        fields = ['id', 'nro_vehiculo', 'hora_salida_ss', 'recorrido_despacho', 'la_planilla']

class ListarDespachosSerial(serializers.ModelSerializer):

    class Meta:
        model = Despacho
        fields = ['id', 'nro_vehiculo', 'detalle', 'hora_salida_ss', 'vuelta', 'nombre_inspector', 'nombre_conductor']

class ListarPlanillasSerial(serializers.ModelSerializer):

    class Meta:
        model = Planilla
        fields = ['id', 'nro_vehiculo', 'nro_control', 'servicio_desc', 'nombre_conductor', 'nro_despachos']

class DespachoImprimirSerial(serializers.ModelSerializer):
    planilla = serializers.CharField(source='control_planilla', read_only=True)
    patente = serializers.CharField(source='patente_vehiculo', read_only=True)
    bus = serializers.CharField(source='nro_vehiculo', read_only=True)
    fecha = serializers.CharField(source='fecha_despacho', read_only=True)
    hora_salida = serializers.CharField(source='hora_salida_ss', read_only=True)
    conductor = serializers.CharField(source='nombre_conductor', read_only=True)
    auxiliar = serializers.CharField(source='nombre_auxiliar', read_only=True)
    inspector = serializers.CharField(source='nombre_inspector', read_only=True)
    variante = serializers.CharField(source='variante_text', read_only=True)

    class Meta:
        model = Despacho
        fields = ['id', 'planilla', 'patente', 'bus', 'fecha', 'hora_salida', 'conductor', 'rut_conductor',
                  'auxiliar', 'rut_auxiliar', 'inspector', 'ruta', 'variante', 'vuelta']

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