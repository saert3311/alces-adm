from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datetime_safe import strftime
from django.views import View
from django.contrib import messages
from recorridos.models import Pago_planilla
from contabilidad.models import Rendicion_cuentas
from django.core.signing import Signer


class RendicionCuentas(LoginRequiredMixin, View):
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
            return render(request, 'inicio.html')

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
                                                                  id_user=request.user.id).values('fecha_pago__date').annotate(total=Sum('valor'))
                if planillas_procesar:
                    datos_validar = [{
                        'fecha': p['fecha_pago__date'].strftime('%d-%m-%Y'),
                        'monto': p['total']
                    } for p in planillas_procesar]
                    if request.POST['firma'] == self.signer.sign_object(datos_validar):
                        #Verificar y guardar
                        rendicion_salvar = {}
                        arqueo_salvar = {}
                        verificar_arqueo = 0
                        for key, value in request.POST.items():
                            if key == 'accion' or key == 'firma':
                                continue
                            if key.isdigit():
                                arqueo_salvar[key] = value if value != '' else 0
                                continue
                            rendicion_salvar[key] = value
                        for key, value in arqueo_salvar.items():
                            verificar_arqueo += int(key)*int(value)
                        if rendicion_salvar['arqueo'] != verificar_arqueo:
                            raise Exception('Arqueo Invalido')
                        print(arqueo_salvar)
                        print(rendicion_salvar)
                        data['yay'] = 'yay'
                        rendicion = Rendicion_cuentas(id_usuario=request.user.id, entregado=rendicion_salvar['total_arqueo'], pendiente=rendicion_salvar['diferencia'], arqueo=arqueo_salvar)
                        rendicion.save()
                        planillas_procesar.update(id_rendicion_cuentas=rendicion)
                        #finaliza la guardacion
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