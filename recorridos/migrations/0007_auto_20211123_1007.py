# Generated by Django 3.2 on 2021-11-23 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_sucursal_es_recaudador'),
        ('recorridos', '0006_alter_pago_planilla_tiene_descuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='terminal_a',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ter_a', to='app.sucursal', verbose_name='Terminal A'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='terminal_b',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ter_b', to='app.sucursal', verbose_name='Terminal B'),
        ),
    ]