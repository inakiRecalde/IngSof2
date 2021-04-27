from django.contrib import admin
from PaginaDePruebaApp.models import *
from PaginaDePruebaApp.models import User 
from .models import User
# Register your models here.

##UserAdmin  adminCombi19 contra: 12345

class clienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email","dni")  #campos de la tabla
    search_fields = ("nombre","apellido")  ## campos por los que se puede buscar
   
   #readonly_fields=('created','updated') 

    #list_filter("") muestra filtros tener en cuaenta para los viajes para filtrar por fechas

admin.site.register(Cliente,clienteAdmin)

admin.site.register(ClienteGold)


admin.site.register(Combi)


admin.site.register(Insumo)

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email","dni","is_staff")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("nombre","apellido")  ## campos por los que se puede buscar

admin.site.register(User, UserAdmin)
