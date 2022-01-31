from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Despacho, Servicio, Planilla, Pago_planilla
from .forms import DespachoForm, ServicioForm, PagarPlanillaForm, BuscarDespachosForm
from .serializers import ListarRecorridoSerial, UltimosDespachosSerial, ListarPlanillasPendientes, DespachoImprimirSerial, ListarDespachosSerial
from django.views.generic import CreateView, UpdateView, TemplateView, View
from datetime import datetime

class ListarServicios(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'recorrido.view_servicio'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'recorridos/listar-servicios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Servicios'
        context['seccion'] = 'recorridos'
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

class CrearServicio(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('recorridos.view_servicio', 'recorridos.add_servicio')
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
        context['seccion'] = 'recorridos'
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

class ActualizarServicio(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('recorridos.view_servicio', 'recorridos.change_servicio')
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
        context['seccion'] = 'recorridos'

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

class AsignarDespacho(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('recorridos.view_despacho', 'recorridos.add_despacho')
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
        context['seccion'] = 'recorridos'
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
                los_ultimos = Despacho.objects.filter(fecha_despacho=datetime.now().date(), id_suc_despacho=request.user.id_sucursal_id).order_by('-hora_asignacion')[:7]
                despachos_serializados = UltimosDespachosSerial(los_ultimos, many=True)
                for i in despachos_serializados.data:
                    data.append(i)
            elif accion == 'buscar_despacho':
                el_despacho = Despacho.objects.get(id=request.POST['despacho'])
                data['despacho'] = DespachoImprimirSerial(el_despacho).data
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class PagoPlanilla(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('recorridos.view_pago_planilla')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'recorridos/pago-planilla.html'
    success_url = reverse_lazy('recorridos:pago-planilla')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Planillas por pagar'
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

class PagarPlanilla(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('recorridos.view_pago_planilla', 'recorridos.add_pago_planilla')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    texto_template = {
    'titulo' : 'Pago Planilla',
    'subtitulo' : 'Complete los datos para registrar el pago',
    'boton' : 'Pagar',
    'seccion2' : 'Vale Pago'
    }

    def get(self, request, *args, **kwargs):
        form = PagarPlanillaForm
        try:
            planilla_pagar = Planilla.objects.get(id=self.kwargs['pl'])
            planilla_enviar = {
                'fecha_planilla' : planilla_pagar.fecha_planilla,
                'fecha_simple' : planilla_pagar.fecha_simple,
                'bus' : planilla_pagar.id_vehiculo.get_identidad,
                'recorrido' : planilla_pagar.id_recorrido.nombre,
                'precio': planilla_pagar.id_recorrido.valor_planilla_feriado(planilla_pagar.fecha_planilla),
                'nro': self.kwargs['pl'],
                'vueltas': planilla_pagar.vueltas,
                'pagada' : planilla_pagar.id_pago_planilla
            }
            if planilla_pagar.id_pago_planilla is not None:
                planilla_enviar['folio'] = planilla_pagar.id_pago_planilla.folio
                planilla_enviar['forma_pago'] = planilla_pagar.id_pago_planilla.tipo_pago.nombre
                planilla_enviar['inspector'] = planilla_pagar.id_user.nombre_completo
        except ObjectDoesNotExist:
            messages.error(self.request, 'Planilla no encontrada')
            return redirect('recorridos:pago-planilla')
        return render(request, 'recorridos/pagar-planilla.html', {
            'planilla': planilla_enviar,
            'form': form,
            'texto' : self.texto_template,
            'seccion' : 'recorridos'
        })

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'pagar_planilla':
                planilla_pagar = Planilla.objects.get(id=self.kwargs['pl'])
                if planilla_pagar.id_pago_planilla is not None:
                    data['error'] = 'Planilla ya fue pagada'
                    return JsonResponse(data, safe=False)
                datos_pago = request.POST
                datos_pago._mutable = True
                datos_pago['valor'] = planilla_pagar.id_recorrido.valor_planilla_feriado(planilla_pagar.fecha_planilla)
                datos_pago['id_user'] = str(request.user.pk)
                datos_pago['pagada'] = True
                datos_pago._mutable = False
                form = PagarPlanillaForm(datos_pago)
                pago_procesado = form.save()
                if 'error' in pago_procesado:
                    data['error'] = pago_procesado['error']
                    return JsonResponse(data, safe=False)
                planilla_pagar.id_pago_planilla = Pago_planilla.objects.get(id=pago_procesado['id_pago_planilla'])
                planilla_pagar.save()
                data['pago_planilla'] = {
                    'nro_planilla' : planilla_pagar.nro_control,
                    'folio' : pago_procesado['id_pago_planilla'],
                    'monto' : pago_procesado['valor_pagado'],
                    'bus' : planilla_pagar.id_vehiculo.get_identidad,
                    'fecha' : pago_procesado['fecha_pago'],
                    'inspector' : str(request.user.nombre_completo),
                    'forma_pago' : planilla_pagar.id_pago_planilla.tipo_pago.nombre,
                    'ruta' : planilla_pagar.id_recorrido.nombre,
                    'fecha_planilla' : planilla_pagar.fecha_planilla
                }
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class InformeDespachos(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'recorridos.view_despacho'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        form = BuscarDespachosForm

        return render(request, 'recorridos/informe-despachos.html', {
            'form': form,
            'titulo' : 'Infome de Despachos Emitidos',
            'seccion' : 'recorridos'
        })

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'listar_despachos':
                data = []
                los_despachos = Despacho.objects.filter(fecha_despacho=datetime.now().date())
                despachos_serializados = ListarDespachosSerial(los_despachos, many=True)
                for i in despachos_serializados.data:
                    data.append(i)
            elif accion == 'buscar':
                data = []
                busqueda = {k: v for k, v in request.POST.items() if v if k != 'accion'}
                busqueda['fecha_despacho'] = datetime.strptime(busqueda['fecha_despacho'], '%d/%m/%Y').date()
                los_despachos = Despacho.objects.filter(**busqueda)
                los_despachos_serializados = ListarDespachosSerial(los_despachos, many=True)
                for i in los_despachos_serializados.data:
                    data.append(i)
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)