from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from PaginaDePruebaApp.models import Cliente, Lugar,User,Chofer,Viaje
from datetime import date
from .forms import CambiarContraForm, EditarForm, UserRegisterForm, LoginForm, ChoferRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.views.generic import FormView

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

def Ahorro (request):
    return render(request,"PaginaDePruebaApp/ahorro.html")

def HistorialDeViajes (request):

    return render(request,"PaginaDePruebaApp/historialDeViajes.html")

def ViajesChofer (request):
    return render(request,"PaginaDePruebaApp/viajesChofer.html")

def Logout_request(request):
    logout(request)
    return redirect(Inicio)

def Login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        usuario = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if usuario is not None:
            login(request,usuario)  
            try: 
                persona=Cliente.objects.get(pk=usuario.id)
            except:  
                return render(request,"PaginaDePruebaApp/inicio.html",{"form":form})
            if persona is not None:
                return render(request,"PaginaDePruebaApp/inicio.html", {"persona": persona})
            else:
                try: 
                    persona=Chofer.objects.get(pk=usuario.id)
                except:  
                    return render(request,"PaginaDePruebaApp/inicio.html",{"form":form})
                if persona is not None:
                    return render(request,"PaginaDePruebaApp/inicio.html", {"persona": persona})
                else:
                    return render(request,"PaginaDePruebaApp/inicio.html", {"persona": persona})
        else:
            return render(request,"PaginaDePruebaApp/login.html",{"form":form})
    else:
        form = LoginForm()
        return render(request,"PaginaDePruebaApp/login.html", {"form": form})

def Registro(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            diccionario=form.cleaned_data
            if mail_disponible(diccionario["email"]):
                if esMayor(diccionario["fechaDeNacimiento"]):
                    usuario = form.save()
                    login(request,usuario)
                    return redirect(Inicio)
                else: 
                    msg ="El usario no es mayor de edad."   ## Mensaje de eeror si es menor
                    form.add_error("fechaDeNacimiento", msg)
                    return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
            else:                
                msg ="Ya existe el mail ingresado."    ## Mensaje si ya existe el correo
                form.add_error("email", msg)
                return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
        else:
            diccionario=form.cleaned_data
            for msg in form.error_messages:
                 messages.error(request, f" {msg}: {form.error_messages[msg]}")
            return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
    else:
        form = UserRegisterForm()
        return render(request,"PaginaDePruebaApp/registro.html", {"form": form})

def RegistroChofer(request):
    if request.method == "POST":
        form = ChoferRegisterForm(request.POST)
        if form.is_valid():
            diccionario=form.cleaned_data
            if mail_disponible(diccionario["email"]):
                usuario = form.save()
                return redirect(Inicio)
            else:                
                msg ="Ya existe el mail ingresado."    ## Mensaje si ya existe el correo
                form.add_error("email", msg)
                return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
        else:
            diccionario=form.cleaned_data
            print(form.error_messages)
            for msg in form.error_messages:
                messages.error(request, f" {msg}: {form.error_messages[msg]}")
            return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
    else:
        form = ChoferRegisterForm()
        return render(request,"PaginaDePruebaApp/registro.html", {"form": form})

<<<<<<< HEAD

def Perfil(request):
    if request.method == "POST":
        usuario = User.objects.get(pk= request.user.id)
        form = EditarForm(request.POST, instance= usuario)
        if form.is_valid():
            form.save()
            return render(request,"PaginaDePruebaApp/perfil.html", {"form": form, 'usuario':usuario})
        else:
            return render(request,"PaginaDePruebaApp/perfil.html", {"form": form})
    else:
        usuario = User.objects.filter(id= request.user.id).first()
        form = EditarForm(instance= usuario)
        return render(request, "PaginaDepruebaApp/perfil.html", {"form": form, 'usuario':usuario})


def CambiarContrasena(request,id_usuario):
    if request.method == "POST":
        usuario = User.objects.get(pk= id_usuario)
        form = PasswordChangeForm(user = usuario, data= request.POST)
        if form.is_valid():
            form.save()
            return redirect(Login)
        else:
            return render(request,"PaginaDePruebaApp/cambiarContrasena.html", {"form": form})
    else:
        usuario = User.objects.filter(id= id_usuario).first()
        form = PasswordChangeForm(user = usuario)
        return render(request, "PaginaDepruebaApp/cambiarContrasena.html", {"form": form, 'usuario':usuario})

=======
def Busqueda(request):
    origen=""
    destino=""
    fecha=""
    if request.GET["origen"]:
        origen=request.GET["origen"]
    if request.GET["destino"]:
        destino=request.GET["destino"]
    if request.GET["fecha"]:
        fecha=request.GET["fecha"]
    if origen and destino and fecha:
        viajes=Viaje.objects.filter(ruta__origen__nombre__icontains=origen, ruta__destino__nombre__icontains=destino, fechaSalida__icontains=fecha)
    elif origen and destino and fecha=="":
        viajes=Viaje.objects.filter(ruta__origen__nombre__icontains=origen, ruta__destino__nombre__icontains=destino)
    elif origen and destino=="" and fecha=="":
        viajes=Viaje.objects.filter(ruta__origen__nombre__icontains=origen)   
    elif origen and destino=="" and fecha:
        viajes=Viaje.objects.filter(ruta__origen__nombre__icontains=origen, fechaSalida__icontains=fecha)  
    elif origen=="" and destino and fecha:
        viajes=Viaje.objects.filter(ruta__destino__nombre__icontains=destino, fechaSalida__icontains=fecha)
    elif origen=="" and destino and fecha=="":
        viajes=Viaje.objects.filter(ruta__destino__nombre__icontains=destino)
    elif origen=="" and destino=="" and fecha:
        viajes=Viaje.objects.filter(fechaSalida__icontains=fecha)
    if origen or destino or fecha:
        return render(request,"PaginaDePruebaApp/busqueda.html", {"viajes":viajes})
    else:
        return render(request,"PaginaDePruebaApp/inicio.html") 
>>>>>>> 9e30029e9af64e3c53803857d57f58a7de019f29
