# Generated by Django 3.2 on 2021-05-21 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='ahorro',
        ),
    ]