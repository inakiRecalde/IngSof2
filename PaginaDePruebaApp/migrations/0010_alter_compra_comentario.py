# Generated by Django 3.2.2 on 2021-05-31 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0009_alter_compra_pendiente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='comentario',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='PaginaDePruebaApp.comentario'),
        ),
    ]
