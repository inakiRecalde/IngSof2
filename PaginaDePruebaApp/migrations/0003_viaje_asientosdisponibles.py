# Generated by Django 3.2 on 2021-05-24 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0002_remove_cliente_ahorro'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaje',
            name='asientosDisponibles',
            field=models.PositiveIntegerField(default=6),
            preserve_default=False,
        ),
    ]