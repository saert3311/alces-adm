# Generated by Django 3.2 on 2021-09-16 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Propietarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('rut', models.CharField(max_length=13, unique=True, verbose_name='RUT')),
                ('direccion', models.CharField(max_length=150)),
                ('comuna', models.IntegerField(verbose_name='Comuna')),
                ('region', models.IntegerField(verbose_name='Region')),
                ('telefono', models.CharField(max_length=9, verbose_name='Telefono')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Correo Electronico')),
                ('activo', models.BooleanField(default=True, verbose_name='Propietario Activo')),
            ],
            options={
                'ordering': ['rut'],
            },
        ),
    ]
