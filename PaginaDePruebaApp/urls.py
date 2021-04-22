from django.urls import path
from PaginaDePruebaApp import views

urlpatterns = [
    path('Inicio', views.Inicio,name = "Inicio"),
    path('Comentarios', views.Comentarios,name = "Comentarios"),
    path('Perfil', views.Perfil,name = "Perfil"),
    path('Contacto', views.Contacto,name = "Contacto"),

]
