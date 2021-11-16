from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import Conductor, Auxiliar
from .serializers import ListarSerializado, AuxiliarSerializado
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ListarConductores(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Conductor
    template_name = 'conductores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Conductores'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'buscardata':
                data = []
                los_conductores = Conductor.objects.all()
                conductores_serializados = ListarSerializado(los_conductores, many=True)
                for i in conductores_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class CrearConductor(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Conductor
    form_class = ConductorForm
    template_name = 'conductores/crear-actualizar.html'
    success_url = reverse_lazy('conductores:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Conductor'
        context['subtitulo'] = 'Complete los datos para crear un nuevo conductor'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            messages.success(request, 'Conductor Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarConductor(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Conductor
    form_class = ConductorForm
    template_name = 'conductores/crear-actualizar.html'
    success_url = reverse_lazy('conductores:listar')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Conductor'
        context['subtitulo'] = 'Puede actualizar la información del usuario'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'directorio'

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            messages.success(request, 'Conductor Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class EliminarConductor(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Conductor
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


class ListarAuxiliares(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Auxiliar
    template_name = 'auxiliares/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Auxiliares'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'buscardata':
                data = []
                los_auxiliares = Auxiliar.objects.all()
                auxiliares_serializados = AuxiliarSerializado(los_auxiliares, many=True)
                for i in auxiliares_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class CrearAuxiliar(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Auxiliar
    form_class = AuxiliarForm
    template_name = 'auxiliares/crear-actualizar.html'
    success_url = reverse_lazy('conductores:listar_auxiliares')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Auxiliar'
        context['subtitulo'] = 'Complete los datos para crear un nuevo auxiliar'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            messages.success(request, 'Auxiliar Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarAuxiliar(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Conductor
    form_class = ConductorForm
    template_name = 'auxiliares/crear-actualizar.html'
    success_url = reverse_lazy('conductores:listar_auxiliares')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Auxiliar'
        context['subtitulo'] = 'Puede actualizar la información del auxiliar'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'directorio'

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            messages.success(request, 'Auxiliar Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)