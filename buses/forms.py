from django import forms
from django.forms import ModelForm, Select
from buses.models import Vehiculo
from propietarios.models import Propietario


class VehiculoForm(ModelForm):
    propietario = forms.ModelChoiceField(queryset=Propietario.objects.all(), widget=forms.Select)

    class Meta:
        model = Vehiculo
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