from django.urls import path
from .views import *

app_name = 'recorridos'

urlpatterns = [
    path('asignarDespacho/', AsignarDespacho.as_view(), name='asignar-despacho'),
    path('informeDespachos/', InformeDespachos.as_view(), name='informe-despachos'),
    path('pagoPlanilla/', PagoPlanilla.as_view(), name='pago-planilla'),
    path('pagoPlanilla/pagar/<int:pl>/', PagarPlanilla.as_view(), name='pagar-planilla'),
    path('administrarServicios/', ListarServicios.as_view(), name='listar-servicios'),
    path('administrarServicios/crear/', CrearServicio.as_view(), name='crear-servicio'),
    path('administrarServicios/actualizar/<int:pk>/', ActualizarServicio.as_view(), name='actualizar-servicio'),
    path('anularPlanilla/', AnularPlanilla.as_view(), name='anular-planilla'),
    path('anularPlanilla/<int:pl>/', AnulacionPlanilla.as_view(), name='planilla-a-anular'),
    path('revalidarPlanilla/', BuscarRevalidarPlanilla.as_view(), name='revalidar-planilla'),
    path('revalidarPlanilla/<int:pl>/', RevalidacionPlanilla.as_view(), name='planilla-a-revalidar'),
    ]