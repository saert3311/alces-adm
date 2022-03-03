from rest_framework import serializers
from .models import Rendicion_cuentas


class RendicionesEnviadasSerial(serializers.ModelSerializer):
    inspector = serializers.CharField(source='nombre_inspector')

    class Meta:
        model = Rendicion_cuentas
        exclude = ['arqueo']