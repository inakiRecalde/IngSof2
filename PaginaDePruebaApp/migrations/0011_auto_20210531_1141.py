# Generated by Django 3.2 on 2021-05-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaginaDePruebaApp', '0010_alter_compra_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='invitados',
        ),
        migrations.AddField(
            model_name='compra',
            name='invitados',
            field=models.ManyToManyField(default=None, null=True, to='PaginaDePruebaApp.Invitado'),
        ),
    ]
