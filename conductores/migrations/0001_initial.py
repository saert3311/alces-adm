# Generated by Django 3.2 on 2021-04-27 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conductores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('rut', models.CharField(max_length=13, unique=True, verbose_name='RUT')),
                ('direccion', models.CharField(max_length=150)),
                ('telefono', models.CharField(max_length=9, verbose_name='Telefono')),
                ('licencia', models.CharField(max_length=20, verbose_name='Tipo de Licencia')),
                ('venc_licencia', models.DateField(verbose_name='Vencimiento de Licencia')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos_conductores')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.region')),
            ],
            options={
                'ordering': ['rut'],
            },
        ),
    ]
