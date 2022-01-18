from django.urls import path
from django.contrib.auth import views as auth_views
from contabilidad.views import RendicionCuentas

app_name = "contabilidad"

urlpatterns = [
    path('rendicionCuentas/', RendicionCuentas.as_view(), name='rendicion-cuentas'),
]
