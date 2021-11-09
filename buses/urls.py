from django.urls import path

from .views import *

app_name = 'buses'

urlpatterns = [
    path('buses/', ListarVehiculos.as_view(), name='listar_vehiculo'),
    path('buses/crear/', CrearVehiculo.as_view(), name='crear_vehiculo'),
    path('buses/actualizar/<int:pk>/', ActualizarVehiculo.as_view(), name='actualizar_vehiculo')
]