from django.db import models
from django.core.exceptions import ValidationError
from alces.settings import MEDIA_URL, STATIC_URL
from app.models import Regiones, Comuna
from datetime import date

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

    def clean(self):
        if self.venc_licencia < date.today():
            raise ValidationError(('La Licencia se encuentra vencida'), code='lic_vencida')

    @property
    def tiene_foto(self):
        if self.foto:
            return True
        return False

    def validez_licencia(self, fecha=date.today()):
        if fecha > self.venc_licencia:
            return False
        delta = fecha - self.venc_licencia
        return delta.days

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
    foto = models.ImageField(upload_to='fotos_auxiliares', null=True, blank=True)

    def __str__(self):
        return self.nombre

    @property
    def tiene_foto(self):
        if self.foto:
            return True
        return False

    @property
    def nombreCompleto(self):
        return '{} {}'.format(self.nombre, self.apellidos)

    @property
    def comuna_text(self):
        if self.comuna:
            return Comuna.objects.get(pk=self.comuna)

    @property
    def foto_url(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        return '{}{}'.format(STATIC_URL, 'img/default-placeholder.png')

    class Meta:
        ordering = ['rut']