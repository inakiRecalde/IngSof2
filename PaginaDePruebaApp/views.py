from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def Inicio (request):

    return render(request,"PaginaDePruebaApp/inicio.html")

def Comentarios (request):

    return render(request,"PaginaDePruebaApp/comentarios.html")

def Perfil (request):

    return render(request,"PaginaDePruebaApp/perfil.html")

def Contacto (request):

    return render(request,"PaginaDePruebaApp/contacto.html")

def Logout_request(request):
    logout(request)
    messages.info(request, "Su sesion cerro correctamente")
    return redirect(Inicio)


def Registro(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request,usuario)
            return redirect(Inicio)
        else:
            for msg in form.error_messages:
                 messages.error(request, f" {msg}: {form.error_messages[msg]}")
    form = UserRegisterForm()
    return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
