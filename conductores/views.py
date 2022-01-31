from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import Conductor, Auxiliar
from .serializers import ListarSerializado, AuxiliarSerializado
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ListarConductores(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'conductores.view_conductor'
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

class CrearConductor(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('conductores.view_conductor', 'conductores.add_conductor')
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
            if not 'error' in data.keys():
                messages.success(request, 'Conductor Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarConductor(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('conductores.view_conductor', 'conductores.change_conductor')
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
            if not 'error' in data.keys():
                messages.success(request, 'Conductor Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ListarAuxiliares(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'conductores.view_auxiliar'
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

class CrearAuxiliar(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('conductores.view_auxiliar', 'conductores.add_auxiliar')
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
            if not 'error' in data.keys():
                messages.success(request, 'Auxiliar Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarAuxiliar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('conductores.view_auxiliar', 'conductores.change_auxiliar')
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
            if not 'error' in data.keys():
                messages.success(request, 'Auxiliar Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)