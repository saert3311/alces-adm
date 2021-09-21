from django import forms
from django.forms import ModelForm, Select
from buses.models import Vehiculos
from propietarios.models import Propietarios


class VehiculoForm(ModelForm):
    propietario = forms.ModelChoiceField(queryset=Propietarios.objects.all(), widget=forms.Select)

    class Meta:
        model = Vehiculos
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