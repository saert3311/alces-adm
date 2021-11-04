# Generated by Django 3.2 on 2021-10-27 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conductores', '0011_auxiliar'),
        ('app', '0011_auto_20211026_1201'),
        ('buses', '0006_auto_20211021_1307'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago_planilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiene_descuento', models.BooleanField(verbose_name='Tiene descuento')),
                ('valor', models.PositiveIntegerField(verbose_name='Monto Pagado')),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Recibido por')),
            ],
        ),
        migrations.CreateModel(
            name='Recorrido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('es_vigente', models.BooleanField(verbose_name='Vigente')),
                ('valor_planilla', models.PositiveIntegerField(verbose_name='Valor planilla')),
                ('distancia', models.SmallIntegerField(verbose_name='Distancia')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25, unique=True, verbose_name='Forma de Pago')),
                ('descripcion', models.CharField(max_length=150, verbose_name='Descripcion')),
                ('es_vigente', models.BooleanField(verbose_name='Vigente')),
            ],
        ),
        migrations.CreateModel(
            name='Planilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_control', models.PositiveIntegerField(unique=True, verbose_name='Nro. Control')),
                ('fecha_venta', models.DateTimeField(auto_now_add=True)),
                ('revalidada', models.PositiveIntegerField(verbose_name='Planilla revalidada')),
                ('es_pirata', models.BooleanField(verbose_name='Es pirata')),
                ('id_conductor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='conductores.conductores', verbose_name='Conductor')),
                ('id_pago_planilla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recorridos.pago_planilla')),
                ('id_recorrido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recorridos.recorrido', verbose_name='Recorrido')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Generado por')),
                ('id_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='buses.vehiculos', verbose_name='Vehiculo')),
            ],
        ),
        migrations.AddField(
            model_name='pago_planilla',
            name='tipo_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recorridos.tipo_pago'),
        ),
        migrations.CreateModel(
            name='Despacho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variante', models.SmallIntegerField(choices=[(1, 'Ida'), (2, 'Vuelta')], default=1, verbose_name='Variante')),
                ('hora_asignacion', models.DateTimeField(auto_now_add=True, verbose_name='Hora Asignación')),
                ('hora_salida', models.DateTimeField(verbose_name='Hora salida')),
                ('hora_llegada', models.DateTimeField(blank=True, verbose_name='Hora llegada')),
                ('id_auxiliar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='conductores.auxiliar', verbose_name='Auxiliar')),
                ('id_conductor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='conductores.conductores', verbose_name='Conductor')),
                ('id_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='llegada', to='app.sucursal', verbose_name='Destino')),
                ('id_origen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='salida', to='app.sucursal', verbose_name='Origen')),
                ('id_planilla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recorridos.planilla', verbose_name='Planilla')),
                ('id_recorrido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recorridos.recorrido', verbose_name='Recorrido')),
                ('id_suc_despacho', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='despachado', to='app.sucursal', verbose_name='Sucursal despacho')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('id_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='buses.vehiculos', verbose_name='Vehiculo')),
            ],
        ),
    ]