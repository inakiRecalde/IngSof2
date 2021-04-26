from django.urls import path
from PaginaDePruebaApp import views

urlpatterns = [
    path('Inicio', views.Inicio,name = "Inicio"),
    path('Comentarios', views.Comentarios,name = "Comentarios"),
    path('Perfil', views.Perfil,name = "Perfil"),
    path('Contacto', views.Contacto,name = "Contacto"),
    path('Registro', views.Registro,name = "Registro"),
    path('logout', views.Logout_request,name = "logout"),
    path('loogin', views.Login_request,name = "login"),
]
