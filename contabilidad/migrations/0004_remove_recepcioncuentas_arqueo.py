# Generated by Django 3.2 on 2022-03-15 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0003_rendicion_cuentas_observaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recepcioncuentas',
            name='arqueo',
        ),
    ]