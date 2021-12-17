from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Despacho, Servicio, Planilla
from .forms import DespachoForm, ServicioForm
from .serializers import ListarRecorridoSerial, UltimosDespachosSerial, ListarPlanillasPendientes
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from datetime import datetime

class ListarServicios(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'recorridos/listar-servicios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Servicios'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'listar':
                data = []
                los_servicios = Servicio.objects.all()
                servicios_serializados = ListarRecorridoSerial(los_servicios, many=True)
                for i in servicios_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class CrearServicio(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Servicio
    form_class = ServicioForm
    template_name = 'recorridos/cu-recorridos.html'
    success_url = reverse_lazy('recorridos:listar-servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Servicio'
        context['subtitulo'] = 'Complete los datos para crear el nuevo servicio'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            if not 'error' in data.keys():
                messages.success(request, 'Servicio Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarServicio(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Servicio
    form_class = ServicioForm
    template_name = 'recorridos/cu-recorridos.html'
    success_url = reverse_lazy('recorridos:listar-servicios')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Servicio'
        context['subtitulo'] = 'Puede actualizar la informacion del servicio'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'directorio'

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            if not 'error' in data.keys():
                messages.success(request, 'Servicio Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class AsignarDespacho(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Despacho
    form_class = DespachoForm
    template_name = 'recorridos/asignar-despacho.html'
    success_url = reverse_lazy('recorridos:asignar-despacho')

    def get_form_kwargs(self):
        result = super().get_form_kwargs()
        result['request'] = self.request
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Asignar Despachos'
        context['seccion1'] = 'Generar'
        context['seccion2'] = 'Ultimos Despachos'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'generar_despacho':
                despacho = request.POST
                despacho._mutable = True
                despacho['id_usuario'] = str(request.user.pk)
                despacho['id_suc_despacho'] = str(request.user.id_sucursal_id)
                if despacho['variante'] == 1:
                    despacho['id_origen'] = str(Servicio.objects.get(pk=despacho['id_recorrido']).terminal_a_id)
                    despacho['id_destino'] = str(Servicio.objects.get(pk=despacho['id_recorrido']).terminal_b_id)
                else:
                    despacho['id_origen'] = str(Servicio.objects.get(pk=despacho['id_recorrido']).terminal_b_id)
                    despacho['id_destino'] = str(Servicio.objects.get(pk=despacho['id_recorrido']).terminal_a_id)
                despacho._mutable = False
                data = []
                form = DespachoForm(despacho, request=request)
                data = form.save()
            elif accion == 'ultimos_despachos':
                data = []
                los_ultimos = Despacho.objects.filter(fecha_despacho=datetime.now().date(), id_suc_despacho=request.user.id_sucursal_id).order_by('-hora_asignacion')[:5]
                despachos_serializados = UltimosDespachosSerial(los_ultimos, many=True)
                for i in despachos_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class PagoPlanilla(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'recorridos/pago-planilla.html'
    success_url = reverse_lazy('recorridos:pago-planilla')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Pago de Planilla'
        context['seccion1'] = 'Buscar'
        context['seccion2'] = 'Planillas por Pagar'
        context['boton'] = 'Pagar'
        context['seccion'] = 'recorridos'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'planillas_pendientes':
                data = []
                las_planillas = Planilla.objects.filter(id_pago_planilla__isnull=True)
                las_planillas_serializadas = ListarPlanillasPendientes(las_planillas, many=True)
                for i in las_planillas_serializadas.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)