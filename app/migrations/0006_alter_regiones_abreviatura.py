# Generated by Django 3.2 on 2021-05-01 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210501_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regiones',
            name='abreviatura',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]