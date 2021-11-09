from django.urls import path
from .views import *

app_name = 'conductores'

urlpatterns = [
    path('conductores/', ListarConductores.as_view(), name='listar_conductores'),
    path('conductores/crear/', CrearConductor.as_view(), name='crear_conductor'),
    path('conductores/actualizar/<int:pk>/', ActualizarConductor.as_view(), name='actualizar_conductor'),
    path('auxiliares/', ListarAuxiliares.as_view(), name='listar_auxiliares'),
    path('auxiliares/crear/', CrearAuxiliar.as_view(), name='crear_auxiliar'),
    path('auxiliares/actualizar/<int:pk>/', ActualizarAuxiliar.as_view(), name='actualizar_auxiliar')
]