# Generated by Django 3.2 on 2021-11-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_sucursal_es_terminal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sucursal',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='lon',
            field=models.DecimalField(decimal_places=7, max_digits=9, null=True),
        ),
    ]
