# Generated by Django 3.2.2 on 2021-06-29 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0023_auto_20210628_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='suspendido',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]