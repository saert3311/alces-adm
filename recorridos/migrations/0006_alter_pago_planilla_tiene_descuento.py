# Generated by Django 3.2 on 2021-11-22 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorridos', '0005_alter_despacho_hora_llegada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago_planilla',
            name='tiene_descuento',
            field=models.BooleanField(default=False, verbose_name='Tiene descuento'),
        ),
    ]
