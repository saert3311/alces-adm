from django.db import models
from cuenta.models import User

# Create your models here.
class RecepcionCuentas(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Nombre Contador')
    fecha = models.DateTimeField(auto_now_add=True)
    entregado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Rendición')
    pendiente = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Rendición', default=0)
    arqueo = models.JSONField(verbose_name='Arqueo de Billetes')
    observaciones = models.TextField(verbose_name='Observaciones')


class Rendicion_cuentas(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Nombre Inspector')
    fecha = models.DateTimeField(auto_now_add=True)
    entregado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Rendición')
    pendiente = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Rendición', default=0)
    arqueo = models.JSONField(verbose_name='Arqueo de Billetes')
    id_recepcion_cuentas = models.ForeignKey(RecepcionCuentas, on_delete=models.PROTECT, verbose_name='Cuenta Recepcionada')

    @property
    def fecha_simple(self):
        return self.fecha.strftime('%d/%m/%Y')

    @property
    def nombre_inspector(self):
        return self.id_usuario.nombre_completo



