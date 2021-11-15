from django import forms
from django.forms import ModelForm
from conductores.models import Conductor, Auxiliar
from .models import Despacho, Servicio

class NombreRutModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{} {} - {}'.format(obj.nombre, obj.apellidos, obj.rut)

class DespachoForm(ModelForm):
    id_conductor = NombreRutModelChoiceField(queryset=Conductor.objects.all())
    id_auxiliar = NombreRutModelChoiceField(queryset=Auxiliar.objects.all())

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
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['id_vehiculo'].es_activo:
            self._errors['Vehiculo'] = self.error_class(['no se encuentra activo'])
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