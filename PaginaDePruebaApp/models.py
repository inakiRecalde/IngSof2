from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    telefono= models.IntegerField(null= True, blank = True)
    dni = models.IntegerField(null= True, blank = True)

class Cliente(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    email= models.EmailField()
    dni= models.IntegerField()
    contraseña = models.CharField(max_length=50)
    suspendido=models.BooleanField(default=False)
    #historialViajes
    #created=models.DateTimeField(auto_now_add=True)
    #updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.nombre)

class Tarjeta():
    nro=models.IntegerField()
    fechaVto=models.DateTimeField()
    codigo=models.IntegerField(max_length=3) 

class ClienteGold(Cliente):
     ahorro=models.FloatField()
    ## created=models.DateTimeField(auto_now_add=True)
    ## updated=models.DateTimeField(auto_now_add=True)
     #faltaria una lista de tarjetas

     def __init__(self):
         Cliente.__init__(self)


class Combi(models.Model):
    #marca=models.CharField(max_length=30)
    modelo=models.CharField(max_length=30)
    cantAsientos= models.IntegerField()
    patente = models.CharField(max_length=20)
    chofer = models.OneToOneField(User, on_delete= models.CASCADE, ## cascade mantiene la integridad referencial ante bajas
                                                null= False, blank = False) ## obliga a que se asigne un chofer
   ## created=models.DateTimeField(auto_now_add=True)
  ##  updated=models.DateTimeField(auto_now_add=True)

class Insumo(models.Model):
    nombre=models.CharField(max_length=30)
    descripcion=models.CharField(max_length=50) #esto sería opcional
    precio=models.IntegerField()
  ##  created=models.DateTimeField(auto_now_add=True)
  ##  updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'el insumo %s tiene un precio de $ %s  ' %(self.nombre, self.precio) ## asi se muestra en la tabla

class Comentario():
    texto=models.CharField(max_length=200)
    puntuacion=models.IntegerField(max_length=1) #no se cómo restringir que el número sea entre 0 y 5
    #autor (un usuario )
  ##  created=models.DateTimeField(auto_now_add=True)
  ##  updated=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return 'Comentario: %s, puntuacion: %d' %(self.texto, self.puntuacion)


class Compra():
    fecha=models.DateTimeField(auto_now_add=True)
    total=models.FloatField()
    #lista de insumos 
    #lista de viajes

class Ruta():
    #origen=
    #destino=
    distancia=models.IntegerField() #distancia en km

class Lugar():
    nombre=models.CharField(max_length=30)
    codigoPostal=models.IntegerField(max_length=4)

class Viaje():
    #pasajeros
    #insumos
    #combi
    #ruta
    fechaSalida=models.DateTimeField()
    fechaLlegada=models.DateTimeField()
    duracion=models.TimeField()
    precio=models.FloatField()
    enCurso=models.BooleanField()
    finalizado=models.BooleanField()