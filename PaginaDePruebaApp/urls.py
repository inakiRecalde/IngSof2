from django.urls import path
from PaginaDePruebaApp import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.Inicio,name = "Inicio"),
    path('Comentarios/', views.Comentarios,name = "Comentarios"),
    path('Perfil/', views.Perfil,name = "Perfil"),
    path('Registro/', views.Registro,name = "Registro"),
    path('RegistroChofer/', views.RegistroChofer,name = "RegistroChofer"),
    path('ViajesChofer/', views.ViajesChofer,name = "ViajesChofer"),
    path('Ahorro/', views.Ahorro,name = "Ahorro"),
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
]
