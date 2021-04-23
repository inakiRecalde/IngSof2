from django.contrib import admin

from PaginaDePruebaApp.models import *

# Register your models here.

##UserAdmin  adminCombi19 contra: 12345

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email","dni")  #campos de la tabla
    search_fields = ("nombre","apellido")  ## campos por los que se puede buscar

    #list_filter("") muestra filtros tener en cuaenta para los viajes para filtrar por fechas
admin.site.register(Usuario, UsuarioAdmin)

admin.site.register(Combi)

admin.site.register(Insumo)

admin.site.register(Chofer)