from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.utils.datetime_safe import strftime
from django.views import View
from django.contrib import messages
from recorridos.models import Pago_planilla


class RendicionCuentas(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

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
            'datos' : datos
        })