from django.urls import path
from PaginaDePruebaApp import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.Inicio,name = "Inicio"),
    path('Comentarios/', views.Comentarios,name = "Comentarios"),
    path('AgregarComentario/<int:compra_id>', views.AgregarComentario,name = "AgregarComentario"),
    path('ModificarComentario/<int:coment_id>', views.ModificarComentario,name = "ModificarComentario"),
    path('Perfil/', views.Perfil,name = "Perfil"),
    path('Registro/', views.Registro,name = "Registro"),
    path('RegistroChofer/', views.RegistroChofer,name = "RegistroChofer"),
    path('ViajesChofer/', views.ViajesChofer,name = "ViajesChofer"),
    path('logout/', views.Logout_request,name = "logout"),
    path('login/', views.Login,name = "login"),
    path('HistorialDeViajes/', views.HistorialDeViajes,name = "HistorialDeViajes"),
    path('Perfil/CambiarContrasena/<int:id_usuario>', views.CambiarContrasena,name = "CambiarContrasena"),
    path('Busqueda/', views.Busqueda,name = "Busqueda" ),
    path('AltaMembresia/', views.AltaMembresia,name = "AltaMembresia" ),
    path('ConfirmacionBajaMembresia/', views.ConfirmacionBajaMembresia,name = "ConfirmacionBajaMembresia" ),
    path('BajaMembresia/', views.BajaMembresia,name = "BajaMembresia" ),
    path('infoViaje/<int:id_viaje>', views.infoViaje, name= "infoViaje"),
    path('Compra/<int:viaje_id>', views.CompraView, name = "Compra" ),
    path('CambioTarjeta/', views.CambioTarjeta, name = "CambioTarjeta" ),
    path('RegistroInvitado/<int:viaje_id>', views.RegistroInvitado, name = "RegistroInvitado" ),
    path('CancelarPasaje/<int:id_viaje>', views.CancelarPasaje, name= "CancelarPasaje"),

    path('EliminarInvitado/<int:invitado_id>/<int:viaje_id>', views.EliminarInvitado, name= "EliminarInvitado"),
    
    path('EliminarInvitado/<str:nombreInsumo>/<int:viaje_id>', views.EliminarInsumo, name= "EliminarInsumo"),
    
    path('AgregarInsumo/<str:nombreInsumo>/<int:viaje_id>', views.AgregarInsumo, name= "AgregarInsumo"),
    path('ListaPasajeros/<int:id_viaje>', views.ListaPasajeros, name= "ListaPasajeros"),

    path('IniciarViaje/<int:id_viaje>', views.IniciarViaje, name="IniciarViaje"),
    path('FinalizarViaje/<int:id_viaje>', views.FinalizarViaje, name="FinalizarViaje"),

    path('NotificarImprevisto/<int:viaje_id>', views.NotificarImprevisto,name = "NotificarImprevisto"),
    path('ModificarImprevisto/<int:imprev_id>', views.ModificarImprevisto,name = "ModificarImprevisto"),
    
    path('CuestionarioCovid/<int:dni>/<int:viaje_id>', views.CuestionarioCovid, name= "CuestionarioCovid"),
    path('Imprevistos/', views.Imprevistos,name = "Imprevistos"),
    path('ConfirmacionImprevistoResuelto/<int:imprev>', views.ConfirmacionImprevistoResuelto,name = "ConfirmacionImprevistoResuelto" ),
    path('MensajeExitoImprevistoResuelto/<int:imprev>', views.ImprevistoResuelto,name = "MensajeExitoImprevistoResuelto" ),
    path('ImprevistosChofer/', views.Imprevistos,name = "ImprevistosChofer" ),
    path('MensajeExitoEliminarImprevisto/<int:imprev>', views.ImprevistoEliminado,name = "MensajeExitoEliminarImprevisto" ),
    path('VerDetalleImprevisto/<int:id_imprev>', views.verDetalleImprevisto,name = "VerDetalleImprevisto" ),
    path('CompraExpress/<int:viaje_id>', views.CompraExpress,name = "CompraExpress" ),  

    ]
