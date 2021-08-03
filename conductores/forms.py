from django import forms
from django.forms import ModelForm, Select

from conductores.models import Conductores
from app.models import Comunas, Regiones


class CrearConductorForm(ModelForm):
    region = forms.ModelChoiceField(queryset=Regiones.objects.all(), widget=forms.Select)

    class Meta:
        model = Conductores
        fields = '__all__'
        widgets = {
            'comuna': Select()
        }

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

class ActualizarConductorForm(ModelForm):
    region = forms.ModelChoiceField(queryset=Regiones.objects.all(), widget=forms.Select)
    comuna = forms.ModelChoiceField(queryset=Comunas.objects.all(), widget=forms.Select)

    class Meta:
        model = Conductores
        fields = '__all__'
        widgets = {
            'comuna': Select()
        }

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