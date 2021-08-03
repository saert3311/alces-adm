from django.forms import ModelForm
from buses.models import Vehiculos


class VehiculoForm(ModelForm):

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