from django import forms
from django.forms import ModelForm, Select

from conductores.models import Conductores
from app.models import Comunas, Regiones


class ConductorForm(ModelForm):
    region = forms.ModelChoiceField(queryset=Regiones.objects.all(), widget=forms.Select)
    comuna = forms.ModelChoiceField(queryset=Comunas.objects.all(), widget=forms.Select)

    class Meta:
        model = Conductores
        fields = '__all__'
        widgets = {
            'comuna': Select(),
            'region': Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        id_comuna = Comunas.objects.get(nombre=cleaned_data['comuna'])
        cleaned_data['comuna'] = id_comuna.id
        id_region = Regiones.objects.get(nombre=cleaned_data['region'])
        cleaned_data['region'] = id_region.id
        return cleaned_data

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
