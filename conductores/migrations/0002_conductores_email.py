# Generated by Django 3.2 on 2021-04-28 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conductores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductores',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Correo Electronico'),
        ),
    ]
