# Generated by Django 3.2 on 2021-11-04 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20211027_1244'),
        ('cuenta', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_sucursal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.sucursal', verbose_name='Sucursal del Usuario'),
        ),
    ]
