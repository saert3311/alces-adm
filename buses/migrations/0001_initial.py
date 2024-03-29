# Generated by Django 3.2 on 2021-05-03 04:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=6, unique=True, verbose_name='Patente')),
                ('u_patente', models.CharField(blank=True, max_length=1, null=True, verbose_name='')),
                ('marca', models.CharField(blank=True, max_length=100, null=True, verbose_name='Marca')),
                ('modelo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Modelo')),
                ('ven_revision', models.DateField(verbose_name='Vencimiento Rev. Tecnica')),
                ('nro', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos_vehiculos')),
            ],
            options={
                'ordering': ['nro'],
            },
        ),
    ]
