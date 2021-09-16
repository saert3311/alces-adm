# Generated by Django 3.2 on 2021-04-27 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('cod_comuna', models.CharField(max_length=5, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'comuna',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('cod_provincia', models.CharField(max_length=3, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'provincia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('cod_region', models.CharField(max_length=2, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'region',
                'managed': False,
            },
        ),
    ]