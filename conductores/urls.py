from django.urls import path
from .views import *

app_name = 'conductores'

urlpatterns = [
    path('conductores/', ListarConductores.as_view(), name='listar'),
    path('conductores/crear/', CrearConductor.as_view(), name='crear'),
    path('conductores/actualizar/<int:pk>/', ActualizarConductor.as_view(), name='actualizar_conductor'),
    path('conductores/eliminar/<int:pk>/', EliminarConductor.as_view(), name='eliminar_conductor')
]