# Generated by Django 4.2.4 on 2023-09-13 00:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_alter_insumo_fechacaducidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='fechaCaducidad',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='fechaCompra',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
