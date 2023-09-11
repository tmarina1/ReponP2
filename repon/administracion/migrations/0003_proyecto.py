# Generated by Django 4.2.4 on 2023-09-07 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_empresa_usuariovinculado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProyecto', models.CharField(max_length=50)),
                ('EstadoProyecto', models.CharField(max_length=30)),
                ('empresaVinculado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.empresa')),
            ],
        ),
    ]
