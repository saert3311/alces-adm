from django.urls import path

from .views import *

app_name = 'conductores'

urlpatterns = [
    path('buses/', ListarVehiculos.as_view(), name='listar'),
    path('buses/crear/', CrearVehiculo.as_view(), name='crear'),
    path('buses/actualizar/<int:pk>/', ActualizarVehiculo.as_view(), name='actualizar'),
    #path('conductores/eliminar/<int:pk>/', EliminarConductor.as_view(), name='eliminar_conductor')
]