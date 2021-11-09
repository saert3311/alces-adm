from django.db import models

from buses.models import Vehiculo
from cuenta.models import User
from conductores.models import Conductor, Auxiliar
from app.models import Sucursal


class Tipo_pago(models.Model):
    nombre = models.CharField(max_length=25, unique=True, verbose_name="Forma de Pago")
    descripcion = models.CharField(max_length=150, verbose_name="Descripcion")
    es_vigente = models.BooleanField(verbose_name="Vigente")


class Pago_planilla(models.Model):
    tiene_descuento = models.BooleanField(verbose_name="Tiene descuento")
    valor = models.PositiveIntegerField(verbose_name="Monto Pagado")
    fecha_pago = models.DateTimeField(auto_now_add=True)
    tipo_pago = models.ForeignKey(Tipo_pago, on_delete=models.PROTECT)
    id_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Recibido por")
    pagada = models.BooleanField(verbose_name="Planilla Pagada", default=False)


class Servicio(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    es_vigente = models.BooleanField(verbose_name="Vigente")
    valor_planilla = models.PositiveIntegerField(verbose_name="Valor planilla")
    distancia = models.SmallIntegerField(verbose_name="Distancia")

    @property
    def kms(self):
        if self.distancia == 1:
            return '{} Km'.format(self.distancia)
        else:
            return '{} Kms'.format(self.distancia)

    def __str__(self):
        return self.nombre


class Planilla(models.Model):
    nro_control = models.PositiveIntegerField(unique=True, verbose_name="Nro. Control")
    fecha_planilla = models.DateField(verbose_name='Fecha de Planilla', default='1999-01-01', blank=False)
    id_pago_planilla = models.ForeignKey(Pago_planilla, on_delete=models.PROTECT)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name="Vehiculo")
    id_recorrido = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name="Recorrido")
    id_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Generado por")
    fecha_venta = models.DateTimeField(auto_now_add=True)
    revalidada = models.PositiveIntegerField(verbose_name="Planilla revalidada")
    id_conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, verbose_name="Conductor")
    es_pirata = models.BooleanField(verbose_name='Es pirata')

class Despacho(models.Model):

    VARIANTE = (
        (1, 'Ida'),
        (2, 'Vuelta')
    )
    id_conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, verbose_name='Conductor')
    id_auxiliar = models.ForeignKey(Auxiliar, on_delete=models.PROTECT, verbose_name='Auxiliar')
    id_planilla = models.ForeignKey(Planilla, on_delete=models.PROTECT, verbose_name='Planilla')
    variante = models.SmallIntegerField(choices=VARIANTE, default=1, verbose_name='Variante')
    hora_asignacion = models.DateTimeField(auto_now_add=True, verbose_name='Hora Asignación')
    fecha_despacho = models.DateField(verbose_name='Fecha Despacho', default='1999-01-01', blank=False)
    hora_salida = models.TimeField(verbose_name='Hora salida')
    hora_llegada = models.TimeField(verbose_name='Hora llegada', blank=True)
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario')
    id_destino = models.ForeignKey(Sucursal, related_name='llegada', on_delete=models.PROTECT, verbose_name='Destino')
    id_recorrido = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name='Recorrido')
    id_origen = models.ForeignKey(Sucursal, related_name='salida', on_delete=models.PROTECT, verbose_name='Origen')
    id_suc_despacho = models.ForeignKey(Sucursal, related_name='despachado', on_delete=models.PROTECT, verbose_name='Sucursal despacho')
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name='Vehiculo')






