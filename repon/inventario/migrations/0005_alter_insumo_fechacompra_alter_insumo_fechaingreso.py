# Generated by Django 4.2.4 on 2023-09-13 02:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_alter_insumo_fechacaducidad_alter_insumo_fechacompra_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='fechaCompra',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 12, 21, 10, 52, 325912)),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='fechaIngreso',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 12, 21, 10, 52, 325912)),
        ),
    ]
