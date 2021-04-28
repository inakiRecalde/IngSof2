from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from PaginaDePruebaApp.models import Cliente,User
from datetime import date
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

# Create your views here.
def envio_Mail(destinatario):
    context = {'destinatario': destinatario}
    template = get_template('PaginaDePruebaApp/correo.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Confirmacion de cuenta',
        'COMBI-19',
        settings.EMAIL_HOST_USER,
        [destinatario]
    )
    email.attach_alternative(content, 'text/html')
    email.send()

def esMayor(nacimiento):
    fecha_actual=date.today()
    resultado=fecha_actual.year - nacimiento.year
    if resultado > 17:
        return True
    return False

def mail_disponible(mail):
    usuarios=User.objects.filter(email=mail)
    if usuarios:
        return False
    return True    

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
            diccionario=form.cleaned_data
            if mail_disponible(diccionario["email"]):
                if esMayor(diccionario["fechaDeNacimiento"]):
                    usuario = form.save()
                    login(request,usuario)
                    #envio_Mail(diccionario["email"])
                    return redirect(Inicio)
                else: 
                    print("El usario no es mayor de edad") #Deberiamos devolver un mensaje de error
                    return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
            else: 
                print("Ya existe el mail ingresado") #Mostrar mensaje de error
                return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
        else:
            diccionario=form.cleaned_data
            print(form.error_messages)
            for msg in form.error_messages:
                 messages.error(request, f" {msg}: {form.error_messages[msg]}")
            return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
    else:
        form = UserRegisterForm()
        return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
