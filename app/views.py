from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .serializers import ListarSucursalesSerializado
from .forms import SucursalForm
from .models import Comuna, Sucursal
from django.contrib import messages

# Create your views here.
from django.views import View


class Inicio(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        return render(request, 'inicio.html')


def handler404(request, exception):
    return render(request, 'page-404.html', status=404)

def handler500(request):
    return render(request, 'page-500.html', status=500)

def GetComunas(request):
    id_region = request.GET.get('region')
    try:
        comunas = Comuna.objects.filter(cod_provincia__cod_region_id=id_region)
        data = []
        for i in comunas:
            data.append({'id': i.id, 'comuna': i.nombre})
    except Exception as e:
        data['error'] =str(e)
    return JsonResponse(data, safe=False)

class ListarSucursales(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    template_name = 'app/listar-sucursales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Sucursales'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'buscardata':
                data = []
                las_sucursales = Sucursal.objects.all()
                sucursales_serializados = ListarSucursalesSerializado(las_sucursales, many=True)
                for i in sucursales_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class CrearSucursal(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    form_class = SucursalForm
    template_name = 'app/cu-sucursales.html'
    success_url = reverse_lazy('app:listar-sucursales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Sucursal'
        context['subtitulo'] = 'Complete los datos para crear una nueva sucursal'
        context['boton'] = 'Crear'
        context['seccion'] = 'directorio'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            messages.success(request, 'Sucursal Creada')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarSucursal(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    form_class = SucursalForm
    template_name = 'app/cu-sucursales.html'
    success_url = reverse_lazy('app:listar-sucursales')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Sucursal'
        context['subtitulo'] = 'Puede actualizar la información de la sucursal'
        context['boton'] = 'Actualizar'
        context['seccion'] = 'directorio'

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            messages.success(request, 'Sucursal Actualizada')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
