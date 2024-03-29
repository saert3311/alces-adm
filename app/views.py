from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .serializers import ListarSucursalesSerializado
from .forms import SucursalForm
from .models import Comuna, Sucursal
from recorridos.models import Despacho, Planilla, Pago_planilla
from django.contrib import messages
from datetime import date
from django.db.models import Count, Sum

# Create your views here.
from django.views import View


class Inicio(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        if request.user.is_superuser is True:
            despachos_emitidos = Despacho.objects.filter(fecha_despacho=date.today()).count()
            maquinas_activas = Despacho.objects.filter(fecha_despacho=date.today()).values('id_vehiculo').distinct().count()
            planillas_emitidas = Planilla.objects.filter(fecha_planilla=date.today()).count()
            recaudacion = Pago_planilla.objects.filter(fecha_pago__date=date.today()).aggregate(Sum('valor'))
        else:
            despachos_emitidos = Despacho.objects.filter(fecha_despacho=date.today(), id_usuario=request.user.id).count()
            maquinas_activas = Despacho.objects.filter(fecha_despacho=date.today(), id_usuario=request.user.id).values('id_vehiculo').distinct().count()
            planillas_emitidas = Planilla.objects.filter(fecha_planilla=date.today(), id_user=request.user.id).count()
            recaudacion = Pago_planilla.objects.filter(fecha_pago__date=date.today(), id_user=request.user.id).aggregate(Sum('valor'))

        return render(request, 'inicio.html', {
            'despachos_emitidos' : despachos_emitidos,
            'maquinas_activas' : maquinas_activas,
            'planillas_emitidas': planillas_emitidas,
            'recaudacion': "$ {:,.0f}".format(recaudacion['valor__sum'] if recaudacion['valor__sum'] != None else 0).replace(',', '.')
        })


def handler404(request, exception):
    return render(request, 'errors/page-404.html', status=404)

def handler500(request):
    return render(request, 'page-500.html', status=500)

def handler403(request, exception):
    return render(request, 'page-403.html', status=403)

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

class ListarSucursales(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'app.view_sucursal'
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

class CrearSucursal(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('app.view_sucursal', 'app.add_sucursal')
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
            if not 'error' in data.keys():
                messages.success(request, 'Sucursal Creada')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class ActualizarSucursal(LoginRequiredMixin, UpdateView):
    permission_required = ('recorridos.view_sucursal', 'recorridos.change_sucursal')
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
            if not 'error' in data.keys():
                messages.success(request, 'Sucursal Actualizada')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
