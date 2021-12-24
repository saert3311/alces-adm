from django.core.exceptions import ValidationError
from django.db import models
from constance import config
from buses.models import Vehiculo
from cuenta.models import User
from conductores.models import Conductor, Auxiliar
from app.models import Sucursal
import datetime
import holidays

def es_terminal(sucursal):
    if not Sucursal.objects.get(pk=sucursal).es_terminal:
        raise ValidationError(
            '%(sucursal) no es terminal',
            params={'sucursal': sucursal}
        )

def inc_control_planilla():
    ultima_planilla = Planilla.objects.all().order_by('id').last()
    if not ultima_planilla:
        return 1
    if config.CAMBIAR_CONTROL is True and config.CONTROL_PLANILLA > ultima_planilla.nro_control:
        return config.CONTROL_PLANILLA
    if config.CAMBIAR_CONTROL is True and config.CONTROL_PLANILLA == ultima_planilla.nro_control:
        config.CAMBIAR_CONTROL = False
    return ultima_planilla.nro_control + 1

class Tipo_pago(models.Model):
    nombre = models.CharField(max_length=25, unique=True, verbose_name="Forma de Pago")
    descripcion = models.CharField(max_length=150, verbose_name="Descripcion")
    es_vigente = models.BooleanField(verbose_name="Vigente")

    def __str__(self):
        return self.nombre


class Pago_planilla(models.Model):
    tiene_descuento = models.BooleanField(verbose_name="Tiene descuento", default=False)
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
    tiempo = models.DurationField(verbose_name='Duracion del Servicio', default=datetime.timedelta(hours=1))
    terminal_a = models.ForeignKey(Sucursal, related_name='ter_a', on_delete=models.PROTECT, verbose_name='Terminal A', default=1, validators=[es_terminal])
    terminal_b = models.ForeignKey(Sucursal, related_name='ter_b', on_delete=models.PROTECT, verbose_name='Terminal B', default=1, validators=[es_terminal])

    @property
    def kms(self):
        if self.distancia == 1:
            return '{} Km'.format(self.distancia)
        else:
            return '{} Kms'.format(self.distancia)

    def __str__(self):
        return self.nombre

    def valor_planilla_feriado(self, fecha=datetime.date.today()):
        if fecha in holidays.Chile() is True or fecha.weekday() == 6:
            return self.valor_planilla / 2
        else:
            return self.valor_planilla



class Planilla(models.Model):
    nro_control = models.PositiveIntegerField(unique=True, verbose_name="Nro. Control", default=inc_control_planilla)
    fecha_planilla = models.DateField(verbose_name='Fecha de Planilla', default='1999-01-01', blank=False)
    id_pago_planilla = models.ForeignKey(Pago_planilla, on_delete=models.PROTECT, blank=True, null=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name="Vehiculo")
    id_recorrido = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name="Recorrido")
    id_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Generado por")
    fecha_venta = models.DateTimeField(auto_now_add=True)
    revalidada = models.PositiveIntegerField(verbose_name="Planilla revalidada", blank=True, null=True)
    id_conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, verbose_name="Conductor")
    es_pirata = models.BooleanField(verbose_name='Es pirata', default=False)

    @property
    def vueltas(self):
        return Despacho.objects.filter(id_planilla=self.id).count()

    @property
    def nro_vehiculo(self):
        return self.id_vehiculo.nro

    @property
    def servicio_desc(self):
        return self.id_recorrido.nombre

    @property
    def valor_planilla(self):
        return self.id_recorrido.valor_planilla

class Despacho(models.Model):

    VARIANTE = (
        (1, 'Ida'),
        (2, 'Vuelta')
    )
    id_conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, verbose_name='Conductor')
    id_auxiliar = models.ForeignKey(Auxiliar, on_delete=models.PROTECT, verbose_name='Auxiliar')
    id_planilla = models.ForeignKey(Planilla, on_delete=models.PROTECT, verbose_name='Planilla', blank=True, null=True)
    variante = models.SmallIntegerField(choices=VARIANTE, default=1, verbose_name='Variante')
    hora_asignacion = models.DateTimeField(auto_now_add=True, verbose_name='Hora Asignación')
    fecha_despacho = models.DateField(verbose_name='Fecha Despacho', default='1999-01-01', blank=False)
    hora_salida = models.TimeField(verbose_name='Hora salida')
    hora_llegada = models.TimeField(verbose_name='Hora llegada', blank=True, null=True)
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario')
    id_destino = models.ForeignKey(Sucursal, related_name='llegada', on_delete=models.PROTECT, verbose_name='Destino')
    id_recorrido = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name='Recorrido')
    id_origen = models.ForeignKey(Sucursal, related_name='salida', on_delete=models.PROTECT, verbose_name='Origen')
    id_suc_despacho = models.ForeignKey(Sucursal, related_name='despachado', on_delete=models.PROTECT, verbose_name='Sucursal despacho')
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name='Vehiculo')

    @property
    def detalle(self):
        return f'{self.id_recorrido.nombre} ({self.get_variante_display()})'

    @property
    def control_planilla(self):
        return self.id_planilla.nro_control

    @property
    def hora_salida_ss(self):
        return self.hora_salida.strftime('%H:%M')

    @property
    def hora_llegada_ss(self):
        return self.hora_llegada.strftime('%H:%M')

    @property
    def nro_vehiculo(self):
        return self.id_vehiculo.nro





