from django.contrib import admin
from PaginaDePruebaApp.models import *
from PaginaDePruebaApp.models import User 
from .models import User
from .forms import CrearChoferForm
# Register your models here.

##UserAdmin  adminCombi19 contra: 12345

admin.site.register(Tarjeta)



class UserAdmin(admin.ModelAdmin):
    model=User
    list_display = ("username", "email","esCliente","esChofer")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("nombre","apellido")  ## campos por los que se puede buscar


admin.site.register(User, UserAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("user", "dni", "suspendido", "esGold")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("nombre","apellido")  ## campos por los que se puede buscar

admin.site.register(Cliente,ClienteAdmin)

class ChoferAdmin(admin.ModelAdmin):
    list_display=("user","telefono")


admin.site.register(Chofer,ChoferAdmin)


class CombiAdmin(admin.ModelAdmin):
    list_display = ("modelo", "cantAsientos","chofer")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("modelo","cantAsientos")  ## campos por los que se puede buscar

admin.site.register(Combi, CombiAdmin)

class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio") 
    search_field = ("nombre")

admin.site.register(Insumo, InsumoAdmin)

class RutaAdmin(admin.ModelAdmin):
    list_display = ("origen", "destino") 
    search_fields = ("origen", "destino")

admin.site.register(Ruta, RutaAdmin)

class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigoPostal") 
    search_fields = ("nombre", "codigoPostal")

admin.site.register(Lugar,LugarAdmin)
class PasajeAdmin(admin.ModelAdmin):
    list_display = ("fecha", "total") 
    search_field = ("fecha")
admin.site.register(Pasaje,PasajeAdmin)

class ViajeAdmin(admin.ModelAdmin):
    list_display = ("ruta","combi") 
    search_field = ("fechaSalida")

admin.site.register(Viaje,ViajeAdmin)

