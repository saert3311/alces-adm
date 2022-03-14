from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView
from .serializers import RendicionesEnviadasSerial
from recorridos.models import Pago_planilla
from contabilidad.models import Rendicion_cuentas
from django.core.signing import Signer


class RendicionCuentas(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('contabilidad.view_rendicion_cuentas', 'contabilidad.add_rendicion_cuentas')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    signer = Signer()

    def get(self, request, *args, **kwargs):
        datos = []
        planillas_procesar = Pago_planilla.objects.filter(id_rendicion_cuentas__isnull=True, id_user=request.user.id).values('fecha_pago__date').annotate(total=Sum('valor'))
        if planillas_procesar:
            datos = [{
                'fecha': p['fecha_pago__date'].strftime('%d-%m-%Y'),
                'monto' : p['total']
            } for p in planillas_procesar]
        else:
            messages.error(request, 'No existen ingresos a declarar')
            return redirect('app:inicio')

        return render(request, 'contabilidad/rendicion-cuentas.html', {
            'seccion' : 'contabilidad',
            'titulo' : 'Rendicion Cuentas Terminal',
            'datos' : datos,
            'firma' : self.signer.sign_object(datos)
        })

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'procesar':
                planillas_procesar = Pago_planilla.objects.filter(id_rendicion_cuentas__isnull=True,
                                                                  id_user=request.user.id)
                if planillas_procesar.exists():
                    planillas_validar = planillas_procesar.values('fecha_pago__date').annotate(total=Sum('valor'))
                    datos_validar = [{
                        'fecha': p['fecha_pago__date'].strftime('%d-%m-%Y'),
                        'monto': p['total']
                    } for p in planillas_validar]
                    if request.POST['firma'] == self.signer.sign_object(datos_validar):
                        #Verificar y guardar
                        rendicion_salvar = {}
                        arqueo_salvar = {}
                        verificar_arqueo = 0
                        for key, value in request.POST.items():
                            if key == 'accion' or key == 'firma':
                                continue
                            if key.isdigit():
                                arqueo_salvar[key] = int(value) if value != '' else 0
                                continue
                            rendicion_salvar[key] = value
                        for key, value in arqueo_salvar.items():
                            verificar_arqueo += int(key)*int(value)
                        if int(rendicion_salvar['total_arqueo']) != verificar_arqueo:
                            raise Exception('Arqueo Invalido, intente nuevamente')

                        rendicion = Rendicion_cuentas(id_usuario=request.user,
                                                      entregado=rendicion_salvar['total_arqueo'],
                                                      pendiente=rendicion_salvar['diferencia'],
                                                      arqueo=arqueo_salvar,
                                                      observaciones=request.POST['observaciones'])
                        rendicion.save()
                        planillas_procesar.update(id_rendicion_cuentas=rendicion)
                        data['rendicion'] = {
                            'inspector': rendicion.id_usuario.nombre_completo,
                            'fecha': rendicion.fecha_simple,
                            'total': rendicion.entregado,
                            'pendiente': rendicion.pendiente,
                            'arqueo': rendicion.arqueo,
                            'folio': rendicion.id
                        }
                    else:
                        data['error'] = 'Se debe actualizar la pagina para realizar rendicion de cuenta'
                        data['recargar'] = True
                else:
                    data['error'] = 'No existen items para rendición de cuentas'
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data, safe=False)

class ListarRendicionesEmitidas(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('contabilidad.view_rendicion_cuentas', 'contabilidad.change_rendicion_cuentas', 'contabilidad.view_recepcion_cuentas','contabilidad.add_recepcion_cuentas')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        datos = Rendicion_cuentas.objects.filter(id_recepcion_cuentas__isnull=True).values('fecha__date', 'id_usuario__id_sucursal__nombre').annotate(total_entregado=Sum('entregado'), total_pendiente=Sum('pendiente'))
        if not datos.exists():
            messages.error(request, 'No existen cuentas para recibir')
            return redirect('app:inicio')

        return render(request, 'contabilidad/listar-rendiciones.html', {
            'seccion' : 'contabilidad',
            'titulo' : 'Recibir Cuentas Terminal',
            'datos' : datos
        })

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'detalle':
                rendiciones = Rendicion_cuentas.objects.filter(fecha__date=request.POST['fecha'], id_recepcion_cuentas__isnull=True)
                if not rendiciones.exists():
                    messages.error(request, 'No Existen rendiciones a recibir en esta fecha')
                    return redirect('contabilidad:recibir-rendicion-listar.html')
                return render(request, 'contabilidad/detalle-rendicion.html', {
                              'seccion' : 'contabilidad',
                              'titulo' : 'Detalle de cuentas recibidas',
                            'rendiciones' : rendiciones
                })
            else:
                data['error'] = 'Metodo no definido'
        except Exception as e:
            data['error'] = str(e)
            if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest' and 'error' in data:
                messages.error(request, str(e))
                return redirect('app:inicio')
        return JsonResponse(data, safe=False)
