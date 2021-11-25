from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from buses.serializers import ListarSerializado
from buses.forms import VehiculoForm
from buses.models import Vehiculo
from django.contrib import messages


class ListarVehiculos(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculo
    template_name = 'buses/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Buses'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'buscardata':
                data = []
                los_vehiculos = Vehiculo.objects.all()
                vehiculos_serializados = ListarSerializado(los_vehiculos, many=True)
                for i in vehiculos_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class CrearVehiculo(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'buses/crear-actualizar.html'
    success_url = reverse_lazy('buses:listar_vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Vehiculo'
        context['subtitulo'] = 'Complete los datos para crear un nuevo Vehiculo'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            if not 'error' in data.keys():
                messages.success(request, 'Vehiculo Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarVehiculo(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'buses/crear-actualizar.html'
    success_url = reverse_lazy('buses:listar_vehiculo')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Vehiculo'
        context['subtitulo'] = 'Puede actualizar la información del Vehiculo'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            if not 'error' in data.keys():
                messages.success(request, 'Vehiculo Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)