from django.forms import ModelForm
from contabilidad.models import Rendicion_cuentas

class RendicionForm(ModelForm):

    class Meta:
        model = Rendicion_cuentas
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