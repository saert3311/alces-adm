# Generated by Django 3.2 on 2021-11-22 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20211116_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='es_recaudador',
            field=models.BooleanField(default=False, verbose_name='Sucursal recibe dinero'),
        ),
    ]