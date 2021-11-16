from django.test import TestCase
from buses.models import Vehiculo
from app.models import Sucursal
from propietarios.models import Propietario
# Create your tests here.

class GenerarDespacho(TestCase):
    def setUp(self):
       Sucursal.objects.create(nombre='Prueba', direccion='Donde sea', lat='1', lon='1', activo=True, es_terminal=True)
       Vehiculo.objects.create(patente='BUENO', marca='Alces', modelo='Bus', ano='2000', ven_revision='01/01/2021', nro='999', foto='hola.jpg', t_salida='1', es_activo='1', id_propietario='1')
       Vehiculo.objects.create(patente='SINFOT', marca='Alces', modelo='Bus', ano='2000', ven_revision='01/01/2021', nro='998', t_salida='1', es_activo='1', id_propietario='1')
       Vehiculo.objects.create(patente='REVVEN', marca='Alces', modelo='Bus', ano='2000', ven_revision='11/15/2021', nro='997',
                       t_salida=Sucursal.objects.get(pk=1), es_activo='1', id_propietario='1')

    def test_verificar_foto(self):
        vehiculo_bueno = Vehiculo.objects.get(patente='BUENO')
        vehiculo_sin_foto = Vehiculo.objects.get(patente='SINFOT')
        self.assertEqual(vehiculo_bueno.foto, 'hola.jpg')
        self.assertFalse(vehiculo_sin_foto.foto)

    def test_verificar_revision(self):
        vehiculo_ven = Vehiculo.objects.get(patente='REVVEN')
        self.assertEqual(vehiculo_ven.validez_revtec(), '1')
        self.assertEqual(vehiculo_ven.validez_revtec(), '1')

    #def test_forms(self):
    #    form_data = {'something': 'something'}
    #    form = MyForm(data=form_data)
    #    self.assertTrue(form.is_valid())