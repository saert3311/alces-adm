from django.core.validators import MinValueValidator
from django.db import models
from propietarios.models import Propietarios

# Create your models here.
from alces.settings import MEDIA_URL, STATIC_URL


class Vehiculos(models.Model):

    TERMINALES = (
        (1, 'Collao'),
        (2, 'Lota'),
        (3, 'Arauco'),
    )
    patente = models.CharField(max_length=6, unique=True, verbose_name="Patente")
    u_patente = models.CharField(max_length=1, null=True, blank=True, verbose_name="")
    marca = models.CharField(max_length=100, verbose_name="Marca", null=True, blank=True)
    modelo = models.CharField(max_length=50, verbose_name="Modelo", null=True, blank=True)
    ano = models.IntegerField(validators=[
        MinValueValidator(2000)
    ], verbose_name="Año", null=True, blank=True)
    ven_revision = models.DateField(verbose_name='Vencimiento Rev. Tecnica')
    nro = models.IntegerField(validators=[
        MinValueValidator(1)
    ], verbose_name="Nro Interno", unique=True)
    foto = models.ImageField(upload_to='fotos_vehiculos', null=True, blank=True)
    t_salida = models.PositiveSmallIntegerField(choices=TERMINALES, default=1, verbose_name="Terminal Salida")
    es_activo = models.BooleanField(default=True, verbose_name="Vehiculo Activo")
    id_propietario = models.ForeignKey(Propietarios, on_delete=models.PROTECT, default=1)

    @property
    def get_patente(self):
        if self.u_patente == "":
            return self.patente
        return f'{self.patente}-{self.u_patente}'

    @property
    def get_descripcion(self):
        return f'{self.marca} {self.modelo}'

    def get_nro(self):
        return self.nro

    @property
    def get_foto(self):
        if self.foto:
            return f'{MEDIA_URL}{self.foto}'
        return f'{STATIC_URL}img/default-placeholder.png'

    @property
    def terminal_display(self):
        return self.get_t_salida_display()

    def __str__(self):
        return f'{self.nro} : {self.patente}'

    class Meta:
        ordering = ['nro']
