from django.urls import path
from django.contrib.auth import views as auth_views
from contabilidad.views import *

app_name = "contabilidad"

urlpatterns = [
    path('rendicionCuentas/', RendicionCuentas.as_view(), name='rendicion-cuentas'),
    path('recibirRendicion/', ListarRendicionesEmitidas.as_view(), name='recibir-rendicion-listar')
]
