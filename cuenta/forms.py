from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import *

from cuenta.models import User


class AuthFormAlces(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'invalido'
        super().__init__(*args, **kwargs)

class CrearUser(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type', 'first_name', 'last_name', 'email', 'id_sucursal', 'groups')


class EditarUsuario(ModelForm):
    widgets = {
        'password': PasswordInput(render_value=True,),
    }
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'user_type', 'is_active', 'id_sucursal', 'groups')
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff']

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