from django.forms import ModelForm
from app.models import Sucursal

class SucursalForm(ModelForm):

    class Meta:
        model = Sucursal
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
