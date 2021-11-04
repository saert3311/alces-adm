from django.db import models

from alces.settings import MEDIA_URL, STATIC_URL
from app.models import Regiones, Comuna

# Create your models here.

class Conductor(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellidos = models.CharField(max_length=50, verbose_name='Apellidos')
    rut = models.CharField(max_length=13, unique=True, verbose_name='RUT')
    direccion = models.CharField(max_length=150)
    comuna = models.IntegerField(verbose_name='Comuna')
    region = models.IntegerField(verbose_name='Region')
    telefono = models.CharField(max_length=9, verbose_name='Telefono')
    email = models.CharField(max_length=50, verbose_name='Correo Electronico', null=True, blank=True)
    licencia = models.CharField(max_length=20, verbose_name='Tipo de Licencia')
    venc_licencia = models.DateField(verbose_name='Vencimiento de Licencia')
    foto = models.ImageField(upload_to='fotos_conductores', null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Conductor Activo")

    def __str__(self):
        return self.nombre

    @property
    def nombreCompleto(self):
        return '{} {}'.format(self.nombre, self.apellidos)

    @property
    def nombrerut(self):
        return '{} {} - {}'.format(self.nombre, self.apellidos, self.rut)

    @property
    def foto_url(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        return '{}{}'.format(STATIC_URL, 'img/default-placeholder.png')

    @property
    def comuna_text(self):
        if self.comuna:
            return Comuna.objects.get(pk=self.comuna)

    class Meta:
        ordering = ['rut']

class Auxiliar(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellidos = models.CharField(max_length=50, verbose_name='Apellidos')
    rut = models.CharField(max_length=13, unique=True, verbose_name='RUT')
    direccion = models.CharField(max_length=150)
    comuna = models.IntegerField(verbose_name='Comuna')
    region = models.IntegerField(verbose_name='Region')
    telefono = models.CharField(max_length=9, verbose_name='Telefono')
    email = models.CharField(max_length=50, verbose_name='Correo Electronico', null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Auxiliar Activo")

    def __str__(self):
        return self.nombre

    @property
    def nombreCompleto(self):
        return '{} {}'.format(self.nombre, self.apellidos)

    @property
    def comuna_text(self):
        if self.comuna:
            return Comuna.objects.get(pk=self.comuna)

    class Meta:
        ordering = ['rut']