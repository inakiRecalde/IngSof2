# Generated by Django 3.2 on 2021-06-24 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0016_invitado_suspendido'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='testRealizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invitado',
            name='testRealizado',
            field=models.BooleanField(default=False),
        ),
    ]
