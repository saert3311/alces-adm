# Generated by Django 3.2 on 2022-02-24 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorridos', '0016_planilla_es_vigente'),
    ]

    operations = [
        migrations.AddField(
            model_name='despacho',
            name='es_vigente',
            field=models.BooleanField(default=True, verbose_name='Esta Vigente'),
        ),
    ]