# Generated by Django 3.2 on 2021-10-26 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_terminales_sucursal'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='lat',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='sucursal',
            name='lon',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
