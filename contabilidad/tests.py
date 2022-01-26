from django.test import TestCase, Client
from django.urls import reverse
from contabilidad.views import RendicionCuentas

# Create your tests here.

class RendicionTest(TestCase):
    fixtures = ['db_precierre.json']


    def test_verificar_rendicion(self):
        c = Client()
        resp = c.post(reverse('RendicionCuentas'), data={
            '20000': 29,
            '2000': '',
            '100': '',
            '10000': '',
            '1000': '',
            '50': '',
            '5000': 1,
            '500': '',
            '10': '',
            'diferencia': 0,
            'firma': 'W3siZmVjaGEiOiIyOC0xMi0yMDIxIiwibW9udG8iOjEzMDAwfSx7ImZlY2hhIjoiMjktMTItMjAyMSIsIm1vbnRvIjoxMzAwMH0seyJmZWNoYSI6IjMwLTEyLTIwMjEiLCJtb250byI6MzM4MDAwfSx7ImZlY2hhIjoiMDMtMDEtMjAyMiIsIm1vbnRvIjoxNDMwMDB9LHsiZmVjaGEiOiIwNC0wMS0yMDIyIiwibW9udG8iOjM5MDAwfSx7ImZlY2hhIjoiMDYtMDEtMjAyMiIsIm1vbnRvIjoxMzAwMH0seyJmZWNoYSI6IjExLTAxLTIwMjIiLCJtb250byI6MjYwMDB9XQ:s9n2ZnmgsM9IVs5bw5xnONmJKh_ACHR_58vKhylFgcg',
            'accion': 'procesar',
            'total_arqueo': 585000,
        })
        print(resp)
        self.assertEqual(resp)

