import datetime

from django import forms
from django.forms import ModelForm
from conductores.models import Conductor, Auxiliar
from .models import Despacho, Servicio, Planilla, Pago_planilla, Tipo_pago
from cuenta.models import User, Sucursal
from buses.models import Vehiculo
from constance import config

class NombreRutModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{} {} - {}'.format(obj.nombre, obj.apellidos, obj.rut)

class DespachoForm(ModelForm):
    id_conductor = NombreRutModelChoiceField(queryset=Conductor.objects.filter(activo=True))
    id_auxiliar = NombreRutModelChoiceField(queryset=Auxiliar.objects.filter(activo=True))
    id_vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.filter(es_activo=True))
    id_recorrido = forms.ModelChoiceField(queryset=Servicio.objects.filter(es_vigente=True))

    class Meta:
        model = Despacho
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid(): #corremos las validaciones en clean()
                despacho = form.save(commit=False)
                despacho.id_planilla, _ = Planilla.objects.get_or_create(
                    id_vehiculo=despacho.id_vehiculo,
                    fecha_planilla=despacho.fecha_despacho,
                    defaults={'id_recorrido': despacho.id_recorrido,
                              'id_user': self.request.user,
                              'id_conductor': despacho.id_conductor})
                despacho.save()
                despacho_generado = Despacho.objects.get(id=despacho.id)
                data['despacho'] = {
                    'id' : despacho_generado.id,
                    'planilla' : despacho.control_planilla,
                    'patente' : despacho_generado.id_vehiculo.patente,
                    'bus': despacho_generado.id_vehiculo.nro,
                    'fecha': despacho_generado.fecha_despacho,
                    'hora_salida' : despacho_generado.hora_salida_ss,
                    'conductor' : despacho_generado.id_conductor.nombreCompleto,
                    'rut_conductor': despacho_generado.id_conductor.rut,
                    'auxiliar': despacho_generado.id_auxiliar.nombreCompleto,
                    'rut_auxiliar': despacho_generado.id_auxiliar.rut,
                    'inspector': self.request.user.nombre_completo,
                    'ruta': despacho_generado.id_recorrido.nombre,
                    'variante': despacho_generado.get_variante_display(),
                    'vuelta': despacho_generado.vuelta
                }
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['id_conductor'].tiene_foto:
            self._errors['Conductor'] = self.error_class(['no tiene fotografia'])
        if not cleaned_data['id_vehiculo'].es_activo:
            self._errors['Vehiculo'] = self.error_class(['no se encuentra activo'])
        if not cleaned_data['id_vehiculo'].validez_revtec():
            self._errors['Vehiculo'] = self.error_class(['tiene revision tecnica vencida'])
        if not cleaned_data['id_conductor'].validez_licencia():
            self._errors['Conductor'] = self.error_class(['tiene licencia vencida'])
        if not cleaned_data['id_conductor'].activo:
            self._errors['Conductor'] = self.error_class(['no se encuentra activo'])
        if not cleaned_data['id_auxiliar'].activo:
            self._errors['Auxiliar'] = self.error_class(['no se encuentra activo'])
        if cleaned_data['variante'] == 1 and self.request.user.id_sucursal_id != Sucursal.objects.get(nombre__icontains='collao').id:
            self._errors['Vehiculo'] = self.error_class(['solo puede generar despachos de vuelta'])
        if Planilla.objects.filter(id_vehiculo=cleaned_data['id_vehiculo']).exclude(fecha_planilla=datetime.date.today()).filter(id_pago_planilla__isnull=True).count() >= config.LIMITE_PLANILLAS_DEUDA:
            self._errors['Vehiculo'] = self.error_class(['adeuda Planilla'])
        if Despacho.objects.filter(id_vehiculo=cleaned_data['id_vehiculo']).filter(fecha_despacho=datetime.date.today()).filter(id_suc_despacho__es_recaudador=True).filter(id_planilla__id_pago_planilla__isnull=True).count() >= config.LIMITE_DESPACHOS_DEUDA:
            self._errors['Vehiculo'] = self.error_class(['Vehiculo debe planilla del dia'])
        if Despacho.objects.filter(id_vehiculo=cleaned_data['id_vehiculo']).filter(fecha_despacho=cleaned_data['fecha_despacho']).count() == 0:
            if cleaned_data['id_vehiculo'].t_salida != cleaned_data['id_origen']:
                self._errors['Vehiculo'] = self.error_class(['1er despacho del Terminal de salida no corresponde'])
        else:
            ultimo_despacho = Despacho.objects.filter(id_vehiculo=cleaned_data['id_vehiculo'], fecha_despacho=cleaned_data['fecha_despacho']).last()
            if ultimo_despacho.variante == cleaned_data['variante']:
                self._errors['Vehiculo'] = self.error_class(['Debe completar su vuelta antes de iniciar una nueva vuelta'])
            momento_ultimo = datetime.datetime.combine(ultimo_despacho.fecha_despacho, ultimo_despacho.hora_salida)
            deberia_llegar = momento_ultimo + Servicio.objects.get(id=cleaned_data['id_recorrido'].id).tiempo
            momento_salida = datetime.datetime.combine(cleaned_data['fecha_despacho'], cleaned_data['hora_salida'])
            if not momento_salida > deberia_llegar:
                self._errors['Vehiculo'] = self.error_class(['Hora de salida del vehiculo no corresponde con tiempo de recorrido anterior'])
            if ultimo_despacho.id_recorrido != cleaned_data['id_recorrido']:
                self._errors['Vehiculo'] = self.error_class([f'Ya tiene una o mas vueltas en ruta {ultimo_despacho.id_recorrido.nombre}'])
            despachos_conductor = Despacho.objects.filter(fecha_despacho=cleaned_data['fecha_despacho'], id_conductor=cleaned_data['id_conductor'])
            for despacho in despachos_conductor:
                if despacho.id_conductor != cleaned_data['id_conductor']:
                    self._errors['Conductor'] = self.error_class([f'Conductor tiene vueltas en el bus {despacho.id_vehiculo.nro}'])
                    break
        return cleaned_data


class ServicioForm(ModelForm):
    terminal_a = forms.ModelChoiceField(queryset=Sucursal.objects.filter(es_terminal=True))
    terminal_b = forms.ModelChoiceField(queryset=Sucursal.objects.filter(es_terminal=True))

    class Meta:
        model = Servicio
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class PagarPlanillaForm(ModelForm):
    tipo_pago = forms.ModelChoiceField(queryset=Tipo_pago.objects.all(), empty_label=None)

    class Meta:
        model = Pago_planilla
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super(PagarPlanillaForm, self)
        try:
            if form.is_valid():
                result = form.save()
                data['id_pago_planilla'] = result.id
                data['valor_pagado'] = result.valor
                data['fecha_pago'] = result.fecha_pago
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data