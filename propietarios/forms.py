from django import forms
from django.forms import ModelForm, Select

from propietarios.models import Propietario
from app.models import Comuna, Regiones


class PropietarioForm(ModelForm):
    region = forms.ModelChoiceField(queryset=Regiones.objects.all(), widget=forms.Select)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), widget=forms.Select)

    class Meta:
        model = Propietario
        fields = '__all__'
        widgets = {
            'comuna': Select(),
            'region': Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        id_comuna = Comuna.objects.get(nombre=cleaned_data['comuna'])
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