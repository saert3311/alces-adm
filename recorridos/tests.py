from django.test import TestCase
from buses.models import Vehiculo
# Create your tests here.

class GenerarDespacho(TestCase):
    def setUp(self):
       Vehiculo.create(patente='BUENO', marca='Alces', modelo='Bus', ano='2000', ven_revision='01/01/2021', nro='999', foto='hola.jpg', t_salida='1', es_activo='1', id_propietario='1')
       Vehiculo.create(patente='SINFOT', marca='Alces', modelo='Bus', ano='2000', ven_revision='01/01/2021', nro='998', t_salida='1', es_activo='1', id_propietario='1')
       Vehiculo.create(patente='REVVEN', marca='Alces', modelo='Bus', ano='2000', ven_revision='11/15/2021', nro='997',
                       t_salida='1', es_activo='1', id_propietario='1')

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