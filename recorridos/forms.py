from django import forms
from django.forms import ModelForm
from conductores.models import Conductor, Auxiliar
from .models import Despacho, Servicio, Planilla
from cuenta.models import User, Sucursal
from buses.models import Vehiculo

class NombreRutModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{} {} - {}'.format(obj.nombre, obj.apellidos, obj.rut)

class DespachoForm(ModelForm):
    id_conductor = NombreRutModelChoiceField(queryset=Conductor.objects.filter(activo=True))
    id_auxiliar = NombreRutModelChoiceField(queryset=Auxiliar.objects.filter(activo=True))
    id_vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.filter(es_activo=True))

    class Meta:
        model = Despacho
        exclude = ['id_planilla', 'id_usuario', 'id_destino', 'id_suc_despacho', 'id_origen', 'hora_llegada']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                despacho = form.save(commit=False)
                despacho.id_suc_despacho = Sucursal.objects.get(pk=self.request.user.id_sucursal_id)
                despacho.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if not cleaned_data['id_conductor'].tiene_foto:
            self._errors['Conductor'] = self.error_class(['no tiene fotografia'])
        if not cleaned_data['id_vehiculo'].es_activo:
            self._errors['Vehiculo'] = self.error_class(['no se encuentra activo'])
        if not cleaned_data['id_vehiculo'].validez_revtec():
            self._errors['Vehiculo'] = self.error_class(['tiene revision tecnica vencida'])
        return cleaned_data


class ServicioForm(ModelForm):

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