# Generated by Django 3.2 on 2021-11-12 14:02

import buses.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_sucursal_es_terminal'),
        ('buses', '0007_rename_vehiculos_vehiculo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='t_salida',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='app.sucursal', validators=[buses.models.es_terminal]),
        ),
    ]
