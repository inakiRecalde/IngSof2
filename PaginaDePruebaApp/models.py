from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.fields import IntegerField
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from PaginaDePruebaApp.validators import *

## CHEACK para aplicar restrincciones mediante expreciones logicas q devuelvan V o F
class CustomUserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):
        
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
    telefono= models.PositiveIntegerField(null= True,blank= False, max_length=10)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name="Chofer"
        verbose_name_plural="Choferes" 

class Combi(models.Model):
    TIPO = (
        ('Comodo', 'Cómodo'),
        ('SuperComodo', 'Súper Comodo'),
    )
    modelo=models.CharField(max_length=30)
    cantAsientos= models.PositiveIntegerField(default=0)
    patente = models.CharField(max_length=20, unique=True)
    chofer = models.OneToOneField(Chofer, on_delete= models.PROTECT)
    tipo=models.CharField(max_length=11,choices=TIPO, default='Comodo')
    
    def __str__(self):
        return "Modelo: {0}, Asientos:{1}, Patente: {2}, Chofer: {3}, Tipo: {4}".format(self.modelo, self.cantAsientos, self.patente, self.chofer,self.tipo)

    class Meta:
        verbose_name="Combi"
        verbose_name_plural="Combis"

    def clean(self):
                
        #se fija si la combi está asignada a algun viaje y hace las validaciones necesarias
        viajesConMismaCombi=Viaje.objects.filter(combi_id=self.id)
        if viajesConMismaCombi:
            combiVieja=Combi.objects.filter(id=viajesConMismaCombi[0].combi_id)
            if self.cantAsientos < combiVieja[0].cantAsientos:
                raise ValidationError("Esta combi se encuentra asignada a un viaje, no se puede modificar la cantidad de asientos a un número menor que el anterior")
            if combiVieja[0].tipo == "SuperComodo" and self.tipo == "Comodo":
                raise ValidationError("Esta combi se encuentra asignada a un viaje, no se puede cambiar el tipo a uno inferior que el anterior")
        

class Insumo(models.Model):
    nombre=models.CharField(max_length=30, unique=True, primary_key=True)
    descripcion=models.CharField(max_length=50) #esto sería opcional
    precio=models.PositiveIntegerField()
    stock=models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return "{0}, Precio: ${1}".format(self.nombre,self.precio)

    class Meta:
        verbose_name="Insumo"
        verbose_name_plural="Insumos" 

    def clean(self):
        viajesConInsumo=Viaje.insumo.through.objects.filter(insumo_id=self.nombre)
        if viajesConInsumo:
            raise ValidationError('La informacion del insumo seleccionado no se puede modificar debido a que esta asignado a un viaje.')       

class Comentario(models.Model):
    texto=models.CharField(max_length=200)
    puntuacion=models.IntegerField() #no se cómo restringir que el número sea entre 0 y 5
    #autor (un usuario )

    def __str__(self):
        return "Comentario: {0}, puntuacion: {1}".format(self.texto, self.puntuacion)

class Lugar(models.Model):
    nombre=models.CharField(max_length=30)
    codigoPostal=models.IntegerField(unique=True, primary_key=True)
    def __str__(self):
        return "{0}({1})".format(self.nombre, self.codigoPostal)

    class Meta:
        verbose_name="Lugar"
        verbose_name_plural="Lugares"

class Ruta(models.Model):
    id = models.AutoField(primary_key=True)
    origen = models.ForeignKey(Lugar, on_delete= models.PROTECT,related_name = 'rutaOrigen')
    destino = models.ForeignKey(Lugar, on_delete= models.PROTECT, related_name = 'rutaDestino')
    distancia=models.PositiveIntegerField() #distancia en km
    descripcion = models.CharField(max_length=50, blank=False)
    def getDescripcion(self):
        return self.descripcion

    def clean(self):
        if self.origen_id == self.destino_id:
            raise ValidationError('Mismo lugar de origen y destino')
        viajesConRuta=Viaje.objects.filter(ruta_id=self.id)
        print(viajesConRuta)
        if viajesConRuta:
            raise ValidationError('La informacion de la ruta seleccionada no se puede modificar debido a que esta asignado a un viaje.')
 
    def __str__(self):
        return "Origen: {0}, Destino: {1}, km: {2}, Des: {3}".format(self.origen, self.destino,self.distancia,self.descripcion)

    class Meta:
        unique_together=('origen','destino','descripcion')  ## hace que no puede haber otra ruta con estos 3 campos iguales
        verbose_name="Ruta"
        verbose_name_plural="Rutas"
        
class Viaje(models.Model):
    enCurso=models.BooleanField(default=False, verbose_name="Viaje iniciado")
    finalizado=models.BooleanField(default=False, verbose_name="Viaje finalizado")
    insumo = models.ManyToManyField(Insumo, verbose_name="Lista de insumos", blank=True)
    combi = models.ForeignKey(Combi, verbose_name="Lista de combis",on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, verbose_name="ruta",on_delete=models.PROTECT)
    fechaSalida=models.DateTimeField()
    fechaLlegada=models.DateTimeField()
    duracion=models.CharField(max_length=20, default='')
    asientosDisponibles=models.PositiveIntegerField()
    precio=models.PositiveIntegerField()   
    

    def clean(self):
        #primero valida que las fechas no sean un string cualquiera así no rompe todo
        if (self.fechaSalida is None) or (self.fechaLlegada is None):
            raise ValidationError('')
        else:

            #se fija si está modificando o agregando un viaje, en el caso de estar modificando entraría al if
            viajeAntes = Viaje.objects.filter(id= self.id)
            if viajeAntes:
                #chequeos en modificar
                if self.enCurso:
                    raise ValidationError('Este viaje no puede modificarse debido a que se encuentra iniciado y/o finalizado')
                else:
                    if( self.combi.patente != viajeAntes[0].combi.patente):
                        if(viajeAntes[0].combi.tipo != self.combi.tipo):
                            if(viajeAntes[0].combi.tipo == 'SuperComodo'):  
                                raise ValidationError('No puede cambiar la combi, solo se puede cambiar por una de tipo igual o superior') 
                        if(self.combi.cantAsientos < viajeAntes[0].combi.cantAsientos): 
                            raise ValidationError('No puede cambiar la combi, solo se puede cambiar por una con mayor o igual cantidad de asientos')
            
            else: # chequeos en agregar
                
                #chequea que las fechas sean a futuro y la de llegada no sea antes que la de salida
                if self.fechaSalida == self.fechaLlegada:
                    raise ValidationError('Las fechas de salida y llegada no pueden ser la misma')
                if self.fechaSalida < timezone.now():
                    raise ValidationError('Fecha de salida inválida')
                if self.fechaLlegada < timezone.now():
                    raise ValidationError('Fecha de llegada inválida')
                if self.fechaLlegada < self.fechaSalida:
                    raise ValidationError('La fecha de llegada debe ser posterior a la de salida')
                self.duracion=(self.fechaLlegada - self.fechaSalida)
                self.asientosDisponibles=(self.combi.cantAsientos)
                print(self.duracion)
                print(self.asientosDisponibles)
            #chequea que no se superpongan las combis , lo hace tanto al modificar o al agregar
            viajesConMismaCombi=Viaje.objects.filter(combi_id=self.combi_id)
            if viajesConMismaCombi is not None:
                for viaje in viajesConMismaCombi:
                    if(viaje.id != self.id):
                        if self.fechaSalida.date() <= viaje.fechaLlegada.date() and self.fechaLlegada.date() >= viaje.fechaSalida.date():
                            raise ValidationError('No se pudo agregar el viaje debido a que ya hay otro viaje con la misma combi dentro de las mismas fechas')

    class Meta:
        verbose_name="Viaje"
        verbose_name_plural="Viajes"

    def __str__(self):
        return "origen: {0}, destino: {1}, combi: {2}, fecha salida: {3}, fecha llegada: {4} y precio: ${5}".format(self.ruta.origen,self.ruta.destino, self.combi.modelo,self.fechaSalida.strftime("%b %d %Y %H:%M"),self.fechaLlegada.strftime("%b %d %Y %H:%M"),self.precio)

class Tarjeta(models.Model):
    nro=models.IntegerField()
    fechaVto=models.DateTimeField()
    codigo=models.IntegerField() 

    class Meta:
        verbose_name="Tarjeta"
        verbose_name_plural="Tarjetas" 

class Cliente(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni= models.IntegerField(null= True, blank = False)
    suspendido=models.BooleanField(default=False)
    esGold=models.BooleanField(default=False)
    historialViajes=models.ManyToManyField(Viaje,default=None,null=True)

    #solo si es gold
    ahorro=models.FloatField(default=0) 
    tarjeta=models.OneToOneField(Tarjeta, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"  

class Invitado(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    dni=models.IntegerField()



class Compra(models.Model):
    fechaCompra=models.DateTimeField(auto_now_add=True)
    total=models.FloatField()
    viaje = models.ForeignKey(Viaje, on_delete= models.CASCADE) 
    user = models.ForeignKey(Cliente, on_delete= models.CASCADE)
    insumos = models.ManyToManyField(Insumo,default=None,null=True,through='CantidadInsumo')
    comentario=models.OneToOneField(Comentario,on_delete=models.SET_NULL,default=None,null=True)
    invitados=models.ManyToManyField(Invitado,default=None,null=True)
    pendiente=models.BooleanField(default=False)
    cancelado=models.BooleanField(default=False)
    class Meta:
        verbose_name="Compra"
        verbose_name_plural="Compras" 

class CantidadInsumo(models.Model):
    compra=models.ForeignKey(Compra,on_delete=models.CASCADE)
    insumo=models.ForeignKey(Insumo,on_delete=models.CASCADE)
    cantidad=models.PositiveIntegerField()
