from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from buses.forms import VehiculoForm
from buses.models import Vehiculos


class ListarVehiculos(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculos
    template_name = 'buses/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Buses'
        context['seccion'] = 'directorio'
        return context

class CrearVehiculo(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculos
    form_class = VehiculoForm
    template_name = 'buses/crear-actualizar.html'
    success_url = reverse_lazy('buses:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Vehiculo'
        context['subtitulo'] = 'Complete los datos para crear un nuevo Vehiculo'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        data = {}
        try:
            form = self.get_form()
            data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarVehiculo(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculos
    form_class = VehiculoForm
    template_name = 'buses/crear-actualizar.html'
    success_url = reverse_lazy('buses:listar')

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
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class EliminarConductor(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Vehiculos
    template_name = 'conductores/eliminar.html'
    success_url = reverse_lazy('conductores:listar')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Conductor'
        context['subtitulo'] = 'Se procedera a la eliminacion del siguiente conductor'
        context['boton'] = 'Eliminar'
        context['seccion'] = 'directorio'
        return context