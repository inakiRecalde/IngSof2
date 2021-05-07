from django.contrib import admin
from PaginaDePruebaApp.models import *
from PaginaDePruebaApp.models import User 
from .models import User
from django.contrib import messages
# Register your models here.

##UserAdmin  adminCombi19 contra: 12345

admin.site.register(Comentario)

admin.site.register(Tarjeta) #esto no debería ir


class UserAdmin(admin.ModelAdmin):
    model=User
    list_display = ("first_name","last_name","email","esCliente","esChofer")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("first_name","last_name")  ## campos por los que se puede buscar
    list_filter = ("esChofer","esCliente")
    actions = ['delete_model']

    #para que no pueda aniadir desde el panel
    def has_add_permission(self, request, obj=None):
        return False

    #esta funcion elimina la accion de eliminar por defecto que tiene django
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    #aca defino una accion de eliminar propia
    @admin.action(description='Eliminar los usuarios seleccionados')
    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            if obj.email=="admin@gmail.com":
                messages.error(request, "El usuario administrador no puede eliminarse")
            else:
                obj.delete()                

admin.site.register(User, UserAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("dni","user", "suspendido", "esGold")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("dni",)  ## campos por los que se puede buscar

    #para que no pueda aniadir desde el panel
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Cliente,ClienteAdmin)

class ChoferAdmin(admin.ModelAdmin):
    list_display=("user","telefono")

    #para que no pueda aniadir desde el panel
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Chofer,ChoferAdmin)


class CombiAdmin(admin.ModelAdmin):
    list_display = ("modelo", "cantAsientos","patente", "chofer")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("modelo",)  ## campos por los que se puede buscar

admin.site.register(Combi, CombiAdmin)

class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio") 
    search_field = ("nombre")

admin.site.register(Insumo, InsumoAdmin)

class RutaAdmin(admin.ModelAdmin):
    list_display = ("origen", "destino","descripcion") 
    search_fields = ("origen", "destino")

admin.site.register(Ruta, RutaAdmin)

class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigoPostal") 
    search_fields = ("nombre", "codigoPostal")

admin.site.register(Lugar,LugarAdmin)

##class PasajeAdmin(admin.ModelAdmin):
##    list_display = ("fecha", "total") 
##    search_field = ("fecha")
##admin.site.register(Pasaje,PasajeAdmin)

class ViajeAdmin(admin.ModelAdmin):
    list_display = ("ruta", "fechaSalida","fechaLlegada","precio") 
    search_field = ("fechaSalida")
    readonly_fields= ("enCurso","finalizado")
    actions = ['delete_model']

    #esta funcion elimina la accion de eliminar por defecto que tiene django
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    #aca defino una accion de eliminar propia
    @admin.action(description='Eliminar los viajes seleccionados')
    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            if obj.enCurso:
                messages.error(request, "El viaje con fecha {0} no puede eliminarse porque se encuentra en curso".format(obj.fechaSalida.strftime("%b %d %Y %H:%M")))
            else:
                obj.delete()

admin.site.register(Viaje,ViajeAdmin)

