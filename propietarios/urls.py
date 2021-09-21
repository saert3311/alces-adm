from django.urls import path
from .views import *

app_name = 'propietarios'

urlpatterns = [
    path('propietarios/', ListarPropietarios.as_view(), name='listar'),
    path('propietarios/crear/', CrearPropietario.as_view(), name='crear'),
    path('propietarios/actualizar/<int:pk>/', ActualizarPropietario.as_view(), name='actualizar')
]