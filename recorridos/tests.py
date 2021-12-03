from django.test import TestCase
from buses.models import Vehiculo
from app.models import Sucursal
from propietarios.models import Propietario
# Create your tests here.

class GenerarDespacho(TestCase):
    fixtures = ['regiones.json', 'provincias.json', 'comunas.json', 'sucursales.json', 'propietarios.json']

    def setUp(self):
       Vehiculo.objects.create(patente='BUENO', marca='Alces', modelo='Bus', ano='2000', ven_revision='2021-01-01', nro='999', foto='hola.jpg', t_salida=Sucursal.objects.get(pk=1), es_activo='1', id_propietario=Propietario.objects.get(pk=1))
       Vehiculo.objects.create(patente='SINFOT', marca='Alces', modelo='Bus', ano='2000', ven_revision='2021-01-01', nro='998', t_salida=Sucursal.objects.get(pk=1), es_activo='1', id_propietario=Propietario.objects.get(pk=1))
       Vehiculo.objects.create(patente='REVVEN', marca='Alces', modelo='Bus', ano='2000', ven_revision='2021-11-01', nro='997',
                       t_salida=Sucursal.objects.get(pk=1), es_activo='1', id_propietario=Propietario.objects.get(pk=1))

    def test_verificar_foto(self):
        vehiculo_bueno = Vehiculo.objects.get(patente='BUENO')
        vehiculo_sin_foto = Vehiculo.objects.get(patente='SINFOT')
        self.assertEqual(vehiculo_bueno.foto, 'hola.jpg')
        self.assertFalse(vehiculo_sin_foto.foto)

    def test_verificar_revision(self):
        vehiculo_ven = Vehiculo.objects.get(patente='REVVEN')
        self.assertFalse(vehiculo_ven.validez_revtec())

    #def test_forms(self):
    #    form_data = {'something': 'something'}
    #    form = MyForm(data=form_data)
    #    self.assertTrue(form.is_valid())