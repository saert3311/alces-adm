# Generated by Django 3.2 on 2022-02-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorridos', '0015_pago_planilla_id_rendicion_cuentas'),
    ]

    operations = [
        migrations.AddField(
            model_name='planilla',
            name='es_vigente',
            field=models.BooleanField(default=True, verbose_name='Esta Vigente'),
        ),
    ]