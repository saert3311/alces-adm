from django.db import models
from django.contrib.auth.models import AbstractUser
from app.models import Sucursal


# Create your models here.
from django.forms import model_to_dict


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'contable'),
        (3, 'terminal'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1, verbose_name="Rol")
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, verbose_name='Sucursal del Usuario', default=1)

    def is_admin(self):
        if self.user_type == 1:
            return True
        else:
            return False

    def is_contable(self):
        if self.user_type == 2:
            return True
        else:
            return False

    def is_terminal(self):
        if self.user_type == 3:
            return True
        else:
            return False

    def toJSON(self):
        item = model_to_dict(self)
        return item

    @property
    def nombre_completo(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        else:
            user = User.objects.get(pk=self.pk)
            if user.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)