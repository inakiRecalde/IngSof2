from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
<<<<<<< HEAD
from PaginaDePruebaApp.validators import *

=======
>>>>>>> 7cacf91468435af53eeecb37fba0033473e2b863
## CHEACK para aplicar restrincciones mediante expreciones logicas q devuelvan V o F
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):
    username=None
    email=models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []
    objects=CustomUserManager()
    esCliente=models.BooleanField(default=False)
    esChofer=models.BooleanField(default=False)

    def __str__(self):
        return "{0}, {1}".format(self.first_name, self.last_name)
        
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"

class Chofer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    telefono= models.IntegerField( null= True,blank= False )
    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name="Chofer"
        verbose_name_plural="Choferes"

class Cliente(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni= models.IntegerField(null= True, blank = False)
    suspendido=models.BooleanField(default=False)
    esGold=models.BooleanField(default=False)
    #historialViajes
    #created=models.DateTimeField(auto_now_add=True)
    #updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

class ClienteGold(Cliente):
     ahorro=models.FloatField(default=0)
    ## created=models.DateTimeField(auto_now_add=True)
    ## updated=models.DateTimeField(auto_now_add=True)
     #faltaria una lista de tarjetas

     def __init__(self):
         Cliente.__init__(self)    

class Tarjeta(models.Model):
    nro=models.IntegerField()
    fechaVto=models.DateTimeField()
    codigo=models.IntegerField() 
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
        verbose_name="Tarjeta"
        verbose_name_plural="Tarjetas"

class Combi(models.Model):
    TIPO = (
        ('Comodo', 'Cómodo'),
        ('SuperComodo', 'Súper Comodo'),
    )
    modelo=models.CharField(max_length=30)
    cantAsientos= models.PositiveIntegerField(default=0)
    patente = models.CharField(max_length=20, unique=True)
    chofer = models.OneToOneField(Chofer, on_delete= models.CASCADE)
    tipo=models.CharField(max_length=11,choices=TIPO, default='Comodo')
   ## created=models.DateTimeField(auto_now_add=True)
  ##  updated=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Modelo: {0}, Asientos: {1}, Chofer: {2}".format(self.modelo, self.cantAsientos,self.chofer)

    class Meta:
        verbose_name="Combi"
        verbose_name_plural="Combis"

class Insumo(models.Model):
    nombre=models.CharField(max_length=30, unique=True, primary_key=True)
    descripcion=models.CharField(max_length=50) #esto sería opcional
    precio=models.DecimalField(max_digits=10, decimal_places=2)
  ##  created=models.DateTimeField(auto_now_add=True)
  ##  updated=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{0}, Precio: ${1}".format(self.nombre,self.precio)

    class Meta:
        verbose_name="Insumo"
        verbose_name_plural="Insumos"

class Comentario(models.Model):
    texto=models.CharField(max_length=200)
    puntuacion=models.IntegerField() #no se cómo restringir que el número sea entre 0 y 5
    #autor (un usuario )
  ##  created=models.DateTimeField(auto_now_add=True)
  ##  updated=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Comentario: {0}, puntuacion: {1}".format(self.texto, self.puntuacion)


class Compra(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    total=models.FloatField()
    #lista de insumos 
    #lista de viajes
    

class Lugar(models.Model):
    nombre=models.CharField(max_length=30)
    codigoPostal=models.IntegerField(unique=True, primary_key=True)
    def __str__(self):
        return "{0}({1})".format(self.nombre, self.codigoPostal)

    class Meta:
        verbose_name="Lugar"
        verbose_name_plural="Lugares"

class Ruta(models.Model):
    origen = models.ForeignKey(Lugar, on_delete= models.CASCADE,related_name = 'rutaOrigen')
    destino = models.ForeignKey(Lugar, on_delete= models.CASCADE, related_name = 'rutaDestino')
    distancia=models.PositiveIntegerField() #distancia en km
    descripcion = models.CharField(max_length=50, blank=False)

<<<<<<< HEAD
=======
    def getDescripcion(self):
        return self.descripcion

    def clean(self):
        if self.origen == self.destino:
            raise ValidationError('Mismo lugar de origen y destino')
            
>>>>>>> 7cacf91468435af53eeecb37fba0033473e2b863
    def __str__(self):
        return "Origen: {0}, Destino: {1}, km: {2}, Des: {3}".format(self.origen, self.destino,self.distancia,self.descripcion)

    class Meta:
        unique_together=('origen','destino','descripcion')  ## hace que no puede haber otra ruta con estos 3 campos iguales
        verbose_name="Ruta"
        verbose_name_plural="Rutas"
        
class Viaje(models.Model):
    
    insumo = models.ManyToManyField(Insumo, verbose_name="Lista de insumos", blank=True)
    combi = models.ForeignKey(Combi, verbose_name="Lista de combis",on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, verbose_name="Lista de rutas",on_delete=models.CASCADE)
    fechaSalida=models.DateTimeField(validators=[validateFechaSalida])
    fechaLlegada=models.DateTimeField(validators=[validateFechaSalida])
    duracion=models.TimeField()
    precio=models.DecimalField(max_digits=10, decimal_places=2,validators=[validatePrecio])
    enCurso=models.BooleanField(default=False)
    finalizado=models.BooleanField(default=False)

    class Meta:
        verbose_name="Viaje"
        verbose_name_plural="Viajes"

    def __str__(self):
        return "ruta: {0}, combi: {1}, fechaSalida: {2}, fechaLlegada: {3}, Precio: ${4}".format(self.ruta, self.combi,self.fechaSalida,self.fechaLlegada,self.precio)

class Pasaje(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    total=models.FloatField()
    viaje = models.ForeignKey(Viaje, on_delete= models.CASCADE) 
    pasajero = models.ForeignKey(User, on_delete= models.CASCADE)
    ##insumo = models.ManyToManyField(Insumo, on_delete= models.CASCADE)
    class Meta:
        verbose_name="Pasaje"
        verbose_name_plural="Pasajes"