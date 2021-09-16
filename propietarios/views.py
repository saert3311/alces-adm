from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import *
from .models import Propietarios
from .serializers import ListarSerializado
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ListarPropietarios(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Propietarios
    template_name = 'propietarios/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Propietarios'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'buscardata':
                data = []
                los_propietarios = Propietarios.objects.all()
                propietarios_serializados = ListarSerializado(los_propietarios, many=True)
                for i in propietarios_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class CrearPropietario(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Propietarios
    form_class = ConductorForm
    template_name = 'propietarios/crear-actualizar.html'
    success_url = reverse_lazy('propietarios:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Propietario'
        context['subtitulo'] = 'Complete los datos para crear un nuevo propietario'
        context['boton'] = 'Crear'
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