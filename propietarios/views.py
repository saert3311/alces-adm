from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PropietarioForm
from .models import Propietario
from .serializers import ListarSerializado
from django.views.generic import ListView, CreateView, UpdateView


class ListarPropietarios(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'propietarios.view_propietario'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Propietario
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
                los_propietarios = Propietario.objects.all()
                propietarios_serializados = ListarSerializado(los_propietarios, many=True)
                for i in propietarios_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)


class CrearPropietario(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('propietarios.view_propietario', 'propietarios.add_propietario')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Propietario
    form_class = PropietarioForm
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
            if not 'error' in data.keys():
                messages.success(request, 'Propietario Creado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class ActualizarPropietario(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('propietarios.view_propietario', 'propietarios.edit_propietario')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Propietario
    form_class = PropietarioForm
    template_name = 'propietarios/crear-actualizar.html'
    success_url = reverse_lazy('propietarios:listar')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Propietario'
        context['subtitulo'] = 'Puede actualizar la información de contacto del propietario'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'directorio'

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            if not 'error' in data.keys():
                messages.success(request, 'Propietario Actualizado')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
