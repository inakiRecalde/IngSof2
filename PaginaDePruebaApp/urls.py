from django.urls import path
from PaginaDePruebaApp import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('Inicio', views.Inicio,name = "Inicio"),
    path('Comentarios', views.Comentarios,name = "Comentarios"),
    path('Perfil', views.Perfil,name = "Perfil"),
    path('Contacto', views.Contacto,name = "Contacto"),
    path('Registro', views.Registro,name = "Registro"),
    path('logout', views.Logout_request,name = "logout"),
    path('login', LoginView.as_view(template_name ='PaginaDePruebaApp/login.html'),name = "login"),
]
