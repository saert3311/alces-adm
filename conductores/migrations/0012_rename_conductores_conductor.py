# Generated by Django 3.2 on 2021-10-27 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recorridos', '0001_initial'),
        ('conductores', '0011_auxiliar'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Conductores',
            new_name='Conductor',
        ),
    ]