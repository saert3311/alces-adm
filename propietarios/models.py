from django.db import models

# Create your models here.
from app.models import Comuna


class Propietario(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellidos = models.CharField(max_length=50, verbose_name='Apellidos')
    rut = models.CharField(max_length=13, unique=True, verbose_name='RUT')
    direccion = models.CharField(max_length=150)
    comuna = models.IntegerField(verbose_name='Comuna')
    region = models.IntegerField(verbose_name='Region')
    telefono = models.CharField(max_length=9, verbose_name='Telefono')
    email = models.CharField(max_length=50, verbose_name='Correo Electronico', null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Propietario Activo")

    def __str__(self):
        return '{} {} - {}'.format(self.nombre, self.apellidos, self.rut)

    @property
    def nombreCompleto(self):
        return '{} {}'.format(self.nombre, self.apellidos)

    @property
    def comuna_text(self):
        if self.comuna:
            return Comuna.objects.get(pk=self.comuna)

    class Meta:
        ordering = ['rut']