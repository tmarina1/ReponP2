# Generated by Django 4.2.4 on 2023-09-08 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0002_perfil_celular_perfil_nombrecargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='celular',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nombreCargo',
            field=models.CharField(max_length=50),
        ),
    ]
