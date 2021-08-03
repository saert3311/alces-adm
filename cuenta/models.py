from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.forms import model_to_dict


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'contable'),
        (3, 'terminal'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1, verbose_name="Rol")

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