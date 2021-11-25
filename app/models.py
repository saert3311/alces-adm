from django.db import models

# Create your models here.
class Regiones(models.Model):
    nombre = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=3, null=True, blank=True)
    capital = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    cod_region = models.ForeignKey(Regiones,  on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    cod_provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=7,  null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=7,  null=True)
    activo = models.BooleanField(default=True, verbose_name='Sucursal Activa')
    es_terminal = models.BooleanField(default=False, verbose_name='Sucursal es terminal')
    es_recaudador = models.BooleanField(default=False, verbose_name='Sucursal recibe dinero')

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def geo(self):
        if self.lat and self.lon:
            return '{},{}'.format(self.lat, self.lon)
        else:
            return 'N/D'