# Generated by Django 3.2 on 2021-05-26 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0004_auto_20210526_1209'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pasaje',
            new_name='Compra',
        ),
        migrations.AlterModelOptions(
            name='compra',
            options={'verbose_name': 'Compra', 'verbose_name_plural': 'Compras'},
        ),
    ]
