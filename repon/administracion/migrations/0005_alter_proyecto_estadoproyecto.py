# Generated by Django 4.2.4 on 2023-09-07 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_rename_empresavinculado_proyecto_empresavinculada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='EstadoProyecto',
            field=models.CharField(max_length=50),
        ),
    ]
