from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class Usuario(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    email= models.EmailField()
    dni= models.IntegerField()
    contraseña = models.CharField(max_length=50)

    def __str__(self):
        return (self.nombre)



class Chofer(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    email= models.EmailField()
    telefono= models.IntegerField()
    contraseña = models.CharField(max_length=50)

    def __str__(self):
        return (self.nombre)


class Combi(models.Model):
    marca=models.CharField(max_length=30)
    modelo=models.CharField(max_length=30)
    cantAsientos= models.IntegerField()
    patente = models.CharField(max_length=20)
    chofer = models.OneToOneField(Chofer, on_delete= models.CASCADE, ## cascade mantiene la integridad referencial ante bajas
                                                null= False, blank = False) ## obliga a que se asigne un chofer


class Insumo(models.Model):
    nombre=models.CharField(max_length=30)
    precio=models.IntegerField()

    def __str__(self):
        return 'el insumo %s tiene un precio de $ %s  ' %(self.nombre, self.precio) ## asi se muestra en la tabla