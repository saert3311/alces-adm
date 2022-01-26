from django.contrib import admin
from django.urls import path
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views

from . import views
from .views import *

app_name = 'app'

urlpatterns = [
    # Pagina Inicio
    path('', Inicio.as_view(), name='inicio'),
    path('tools/get_comunas/', views.GetComunas, name='get_comunas'),
    path('sucursales/', ListarSucursales.as_view(), name='listar-sucursales'),
    path('sucursales/crear/', CrearSucursal.as_view(), name='crear-sucursal'),
    path('sucursales/actualizar/<int:pk>/', ActualizarSucursal.as_view(), name='actualizar-sucursal')
]