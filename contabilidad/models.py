from django.db import models
from cuenta.models import User
import datetime

# Create your models here.

class Rendicion_cuentas(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Nombre Inspector')
    fecha = models.DateTimeField(auto_now_add=True)
    entregado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Rendición')
    pendiente = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Rendición', default=0)
    arqueo = models.JSONField(verbose_name='Arqueo de Billetes')

    @property
    def fecha_simple(self):
        return self.fecha_pago.strftime('%d/%m/%Y')
