# Generated by Django 3.2 on 2021-05-01 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conductores', '0003_auto_20210501_0025'),
        ('app', '0003_comunas_provincias_regiones'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comuna',
        ),
        migrations.DeleteModel(
            name='Provincia',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.AddField(
            model_name='provincias',
            name='cod_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.regiones'),
        ),
        migrations.AddField(
            model_name='comunas',
            name='cod_provincia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.provincias'),
        ),
    ]
