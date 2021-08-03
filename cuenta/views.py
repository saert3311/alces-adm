from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from .forms import AuthFormAlces, CrearUser, EditarUsuario
from .models import User


# Create your views here.
class Login(LoginView):
    template_name = 'cuenta/login.html'
    authentication_form = AuthFormAlces

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        respuesta = {}
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.get('remember'):
                    request.session.set_expiry(0)
                respuesta['msg'] = 'success'
            else:
                respuesta['msg'] = 'inactive'
        else:
            respuesta['msg'] = 'invalid'
        return JsonResponse(respuesta)


class ListarUsuarios(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Usuarios'
        context['seccion'] = 'admin'
        return context


class CrearUsuario(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = CrearUser
    template_name = 'cuenta/crear-actualizar.html'
    success_url = reverse_lazy('cuenta:usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Usuario'
        context['subtitulo'] = 'Complete los datos para la creacion del nuevo usuario'
        context['boton'] = 'Crear'
        context['seccion'] = 'admin'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = CrearUser(request.POST)
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarUsuario(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = EditarUsuario
    template_name = 'cuenta/crear-actualizar.html'
    success_url = reverse_lazy('cuenta:usuarios')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Usuario'
        context['subtitulo'] = 'Puede editar la información o permisos del usuario'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'admin'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class EliminarUsuario(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'cuenta/eliminar.html'
    success_url = reverse_lazy('cuenta:usuarios')

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
        context['titulo'] = 'Eliminar Usuario'
        context['subtitulo'] = 'Se procedera a la eliminacion del siguiente usuario'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'admin'
        return context