# Generated by Django 3.2 on 2021-11-25 13:18

from django.db import migrations, models
import django.db.models.deletion
import recorridos.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_sucursal_es_recaudador'),
        ('recorridos', '0007_auto_20211123_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planilla',
            name='es_pirata',
            field=models.BooleanField(default=False, verbose_name='Es pirata'),
        ),
        migrations.AlterField(
            model_name='planilla',
            name='nro_control',
            field=models.PositiveIntegerField(default=recorridos.models.inc_control_planilla, unique=True, verbose_name='Nro. Control'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='terminal_a',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ter_a', to='app.sucursal', validators=[recorridos.models.es_terminal], verbose_name='Terminal A'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='terminal_b',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ter_b', to='app.sucursal', validators=[recorridos.models.es_terminal], verbose_name='Terminal B'),
        ),
    ]
