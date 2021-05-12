from django.contrib import admin
from PaginaDePruebaApp.models import *
from PaginaDePruebaApp.models import User 
from .models import User
from django.contrib import messages
# Register your models here.

##UserAdmin  adminCombi19 contra: 12345

#admin.site.register(Comentario) #esto lo implementamos en otra demo

#admin.site.register(Tarjeta) #esto no debería ir, el admin no debería poder ver las tarjetas 


class UserAdmin(admin.ModelAdmin):
    model=User
    fields=("first_name","last_name","email","esCliente","esChofer")
    list_display = ("first_name","last_name","email","esCliente","esChofer")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("first_name","last_name")  ## campos por los que se puede buscar
    list_filter = ("esChofer","esCliente")
    actions = ['delete_model']
    readonly_fields=("first_name","last_name","email")

    #para que no pueda aniadir desde el panel
    def has_add_permission(self, request, obj=None):
        return False

    #esto es para que no aparezca el boton de eliminar cuando entrás a una instancia
    def has_delete_permission(self,request, obj=None):
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
                if obj.esChofer:
                    combisChof=Combi.objects.filter(chofer_id=obj.id)
                    if combisChof:
                        messages.error(request, "El chofer {0} no puede eliminarse porque se encuentra asignada/o a una combi".format(obj.first_name))
                    else:
                        obj.delete()
                else:
                    obj.delete() 
                           

admin.site.register(User, UserAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("dni","user", "suspendido", "esGold")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("dni",)  ## campos por los que se puede buscar
    readonly_fields=("user","dni")

    #para que no pueda aniadir desde el panel
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Cliente,ClienteAdmin)

class ChoferAdmin(admin.ModelAdmin):
    list_display=("user","telefono")
    readonly_fields=("user",)

    #para que no pueda aniadir desde el panel
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Chofer,ChoferAdmin)


class CombiAdmin(admin.ModelAdmin):
    list_display = ("modelo", "cantAsientos","patente", "chofer")  #Campos que va a mostrar cuando presione Usuarios
    search_fields = ("modelo",)  ## campos por los que se puede buscar

    #actions agrega la opcion de eliminar propia
    actions=['delete_model']
    #esto es para que no aparezca el boton de eliminar cuando entrás a una instancia
    def has_delete_permission(self,request, obj=None):
        return False
    #aca saco la opcion de eliminar por defecto    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    #aca hago un eliminar propio
    @admin.action(description='Eliminar las combis seleccionadas')  
    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            viajesConCombi=Viaje.objects.filter(combi_id=obj.id)
            if viajesConCombi:
                messages.error(request, "La combi {0} no puede eliminarse porque se encuentra asignada a un viaje".format(obj.modelo))
            else:
                obj.delete()  

admin.site.register(Combi, CombiAdmin)

class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio") 
    search_field = ("nombre")
    actions=['delete_model']

    #esto es para que no aparezca el boton de eliminar cuando entrás a una instancia
    def has_delete_permission(self,request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @admin.action(description='Eliminar los insumos seleccionados')  
    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            viajesConInsumo=Viaje.insumo.through.objects.filter(insumo_id=obj.nombre)
            if viajesConInsumo:
                messages.error(request, "El insumo {0} no puede eliminarse porque se encuentra asignada/o a un viaje".format(obj.nombre))
            else:
                obj.delete()   

admin.site.register(Insumo, InsumoAdmin)

class RutaAdmin(admin.ModelAdmin):
    list_display = ("origen", "destino","descripcion") 
    search_fields = ("origen", "destino")

    #actions agrega la opcion de eliminar propia
    actions=['delete_model']
    #esto es para que no aparezca el boton de eliminar cuando entrás a una instancia
    def has_delete_permission(self,request, obj=None):
        return False
    #aca saco la opcion de eliminar por defecto    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    #aca hago un eliminar propio
    @admin.action(description='Eliminar las rutas seleccionadas')  
    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            viajesConRuta=Viaje.objects.filter(ruta_id=obj.id)
            if viajesConRuta:
                messages.error(request, "La ruta {0} no puede eliminarse porque se encuentra asignada a un viaje".format(obj.descripcion))
            else:
                obj.delete()  

admin.site.register(Ruta, RutaAdmin)

class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigoPostal") 
    search_fields = ("nombre", "codigoPostal")

    #actions agrega la opcion de eliminar propia
    actions=['delete_model']
    #esto es para que no aparezca el boton de eliminar cuando entrás a una instancia
    def has_delete_permission(self,request, obj=None):
        return False
    #aca saco la opcion de eliminar por defecto    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    #aca hago un eliminar propio
    @admin.action(description='Eliminar los lugares seleccionados')  
    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            rutasConLugarDestino=Ruta.objects.filter(destino_id=obj.codigoPostal)
            rutasConLugarOrigen=Ruta.objects.filter(origen_id=obj.codigoPostal)
            if rutasConLugarDestino or rutasConLugarOrigen:
                messages.error(request, "El lugar {0} no puede eliminarse porque se encuentra asignado a una ruta".format(obj.nombre))
            else:
                obj.delete()  

admin.site.register(Lugar,LugarAdmin)

class ViajeAdmin(admin.ModelAdmin):
    list_display = ("get_ruta", "fechaSalida","fechaLlegada","get_combi","precio","enCurso","finalizado") 
    readonly_fields= ("enCurso","finalizado","duracion")
    actions = ['delete_model']
    list_filter = ("finalizado","enCurso")
    filter_horizontal = ('insumo',)

    #este metodo es para que, en vez de mostrar todo el objeto, muestre solo el modelo de la combi en la lista de viajes
    def get_combi(self,obj):
        return obj.combi.modelo
    get_combi.short_description='Combi'
    get_combi.admin_order_field='modelo__combi'

    #este metodo es para que, en vez de mostrar todo el objeto, muestre solo la descripcion de la ruta en la lista de viajes
    def get_ruta(self,obj):
        return obj.ruta.descripcion
    get_ruta.short_description='Ruta'
    get_ruta.admin_order_field='descripcion__ruta'

    #esto es para que no aparezca el boton de eliminar cuando entrás a una instancia
    def has_delete_permission(self,request, obj=None):
        return False

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

