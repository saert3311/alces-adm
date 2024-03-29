# Generated by Django 3.2 on 2022-01-17 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rendicion_cuentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('entregado', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Rendición')),
                ('pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto Rendición')),
                ('arqueo', models.JSONField(verbose_name='Arqueo de Billetes')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Nombre Inspector')),
            ],
        ),
    ]
