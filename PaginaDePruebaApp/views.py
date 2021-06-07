from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from PaginaDePruebaApp.models import CantidadInsumo, Cliente, Lugar,User,Chofer,Viaje,Insumo,Compra
from datetime import date
from .forms import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

# metodos.
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

def chequearVencimiento(fecha):
    fechaActual=date.today()
    if fecha<fechaActual:
        return False
    return True

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

def getInvitadosCompra(id_compra):
    compraInvitadosQuery=Compra.invitados.through.objects.filter(compra_id=id_compra)
    id_invitados=compraInvitadosQuery.values_list('invitado_id')
    invitadosQuery=Invitado.objects.filter(pk__in=id_invitados)
    return list(invitado for invitado in invitadosQuery)

def getInsumosCompra(id_compra):
    compraInsumosQuery=Compra.insumos.through.objects.filter(compra_id=id_compra)
    id_insumos=compraInsumosQuery.values_list('insumo_id')
    insumosQuery=Insumo.objects.filter(pk__in=id_insumos)
    return list(insumo for insumo in insumosQuery)

def getInsumosViaje(id_viaje):
    viajeInsumosQuery=Viaje.insumo.through.objects.filter(viaje_id=id_viaje)
    id_insumos=viajeInsumosQuery.values_list('insumo_id')
    insumosQuery=Insumo.objects.filter(pk__in=id_insumos)
    return list(insumo for insumo in insumosQuery)

def aplicarDescuento(precio):
    descuento=(precio/100)*10
    return precio-descuento

def calcularPrecioInsumos(insumosCompraConCantidad):
    suma=0
    for i in range(0,len(insumosCompraConCantidad)):
        suma=suma+(insumosCompraConCantidad[i][0].precio*insumosCompraConCantidad[i][1])

    return suma

def getInvitadosViaje(viaje_id):
    comprasViaje=Compra.objects.filter(viaje_id=viaje_id)
    comprasIds=list(compra.id for compra in comprasViaje)
    invitadosViajeQuery=Compra.invitados.through.objects.filter(compra_id__in=comprasIds)
    invitadosIds=list(invitado.invitado_id for invitado in invitadosViajeQuery)
    invitadosViaje=Invitado.objects.filter(id__in=invitadosIds)
    invitadosDnis=list(invitado.dni for invitado in invitadosViaje)
    return invitadosDnis

def getInsumosConCantidad(listaInsumos,compra):
    insumosCantidadQuery=CantidadInsumo.objects.filter(compra_id=compra.id,insumo__in=listaInsumos)
    listaCantidades=list(cantInsumo.cantidad for cantInsumo in insumosCantidadQuery)
    return list(zip(listaInsumos,listaCantidades))


#views 
def Inicio (request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.user.esChofer:
            persona=Chofer.objects.get(user_id=request.user.id)
        else:
            persona=Cliente.objects.get(user_id=request.user.id) 
        return render(request,"PaginaDePruebaApp/inicio.html", {"persona":persona})
    else:
        return render(request,"PaginaDePruebaApp/inicio.html")

def ModificarComentario(request,coment_id):

    if request.method== "POST":
        form= ComentInputForm(request.POST)
        if form.is_valid():
            compra = Compra.objects.get(comentario_id = coment_id)
            form.save(compra)

            comentViejo = Comentario.objects.get(pk = coment_id)
            comentViejo.delete()
            
            compras = Compra.objects.all()
            comentarios = Comentario.objects.all()
            return redirect(Comentarios)
        else:        
            return render(request,"PaginaDePruebaApp/modificarComentario.html", {"form": form})
    else:
        if request.method== "GET":
            coment = Comentario.objects.get(pk=coment_id)
            form= ComentInputForm(instance= coment)
            return render(request,"PaginaDePruebaApp/modificarComentario.html", {"form": form})     
          
def AgregarComentario(request,compra_id):
    if request.method== "POST":
        form= ComentInputForm(request.POST)
        if form.is_valid():
            compra= Compra.objects.get(pk = compra_id)
            form.save(compra)
            return redirect(Comentarios)
        else:        
            return render(request,"PaginaDePruebaApp/agregarComentario.html", {"form": form})
    else:
        form= ComentInputForm()
        return render(request,"PaginaDePruebaApp/agregarComentario.html", {"form": form})

def Comentarios (request):
    if request.method== "POST":
        pk = request.POST.get('identificador_id')
        coment = Comentario.objects.get(pk=pk)
        coment.delete()
        comentarios = Comentario.objects.all()
        compras = Compra.objects.all()
        return redirect(Comentarios)
    else:
        comentarios = Comentario.objects.all()
        compras = Compra.objects.all()
        if not request.user.is_staff:
            if request.user.esCliente:
                persona=Cliente.objects.get(user_id=request.user.id) 
                return render(request,"PaginaDePruebaApp/comentarios.html", {"comentarios": comentarios, "compras": compras,"user_id":request.user.id,"persona":persona})        
        return render(request,"PaginaDePruebaApp/comentarios.html", {"comentarios": comentarios, "compras": compras,"user_id":request.user.id})

def Ahorro (request):
    if request.user.is_authenticated:
        persona=Cliente.objects.get(user_id=request.user.id) 
        persona=Cliente.objects.get(user_id=request.user.id)
        return render(request,"PaginaDePruebaApp/ahorro.html", {"persona":persona}) 
    else:
        return render(request,"PaginaDePruebaApp/ahorro.html")

def HistorialDeViajes(request):
    if request.user.is_authenticated:
        compras=Compra.objects.filter(user__user__id__icontains=request.user.id)
        persona=Cliente.objects.get(user_id=request.user.id) 
        if compras:
            return render(request,"PaginaDePruebaApp/historialDeViajes.html", {"compras":compras,"persona":persona})       
        else:
            return render(request,"PaginaDePruebaApp/historialDeViajes.html",{"persona":persona})

def AltaMembresia (request):
    if request.method== "POST":
        form= TarjetaForm(request.user, request.POST)
        if form.is_valid():
            diccionario=form.cleaned_data
            if chequearVencimiento(diccionario["fechaVto"]):
                tarjeta=form.save()
                cliente=Cliente.objects.get(user_id=request.user.id)
                cliente.esGold=True
                cliente.tarjeta=tarjeta
                cliente.save()
                return render(request,"PaginaDePruebaApp/mensajeExitoMembresia.html")
            else:
                msg ="La tarjeta se encuentra vencida"   ## Mensaje de error si esta vencida la tarjeta
                form.add_error("fechaVto", msg)
                return render(request,"PaginaDePruebaApp/altaMembresia.html", {"form": form})
        else:        
            return render(request,"PaginaDePruebaApp/altaMembresia.html", {"form": form})
    else:
        form = TarjetaForm(request.user)
        return render(request,"PaginaDePruebaApp/altaMembresia.html", {"form": form})

def CambioTarjeta (request):
    if request.method== "POST":
        form= TarjetaForm(request.user, request.POST)
        if form.is_valid():
            diccionario=form.cleaned_data
            if chequearVencimiento(diccionario["fechaVto"]):
                tarjeta=form.save()
                return render(request,"PaginaDePruebaApp/mensajeCambioTarjeta.html")
            else:
                msg ="La tarjeta se encuentra vencida"   ## Mensaje de error si esta vencida la tarjeta
                form.add_error("fechaVto", msg)
                return render(request,"PaginaDePruebaApp/altaMembresia.html", {"form": form})
        else:        
            return render(request,"PaginaDePruebaApp/altaMembresia.html", {"form": form})
    else:
        form = TarjetaForm(request.user)
        return render(request,"PaginaDePruebaApp/altaMembresia.html", {"form": form})

def ConfirmacionBajaMembresia(request):
    return render(request, "PaginaDePruebaApp/confirmacionBajaMembresia.html")


def BajaMembresia(request):
    persona=Cliente.objects.get(user_id=request.user.id)
    persona.tarjeta=None
    persona.esGold=False
    persona.save()
    return render(request, "PaginaDePruebaApp/bajaMembresia.html")

def infoViaje(request, id_viaje):
    viaje = Viaje.objects.get(pk=id_viaje)
    viajeInsumosQuery=Viaje.insumo.through.objects.filter(viaje_id=id_viaje)
    insumos=list(Insumo.objects.get(pk=viajeInsumo.insumo_id) for viajeInsumo in viajeInsumosQuery)
    if request.user.is_authenticated:
        compras = Compra.objects.filter(viaje__id__icontains=id_viaje, user__user__id__icontains=request.user.id)
        if compras:
            for compra in compras:
                if not compra.cancelado:
                    insumosComprados=getInsumosCompra(compra.id)
                    insumosCompradosConCantidad=getInsumosConCantidad(insumosComprados,compra)
                    #En el return de abajo faltaria mandar los insumos comprados por parametro   
                    invitados=getInvitadosCompra(compra.id) 
                    return render(request,"PaginaDePruebaApp/infoViaje.html",{"viaje": viaje,"insumos":insumos,"compra":compra,"invitados":invitados,"insumosCompradosConCantidad":insumosCompradosConCantidad})
                return render(request,"PaginaDePruebaApp/infoViaje.html",{"viaje": viaje,"insumos":insumos,"compra":compra})
    return render(request,"PaginaDePruebaApp/infoViaje.html",{"viaje": viaje,"insumos":insumos})    

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
            for msg in form.error_messages:
                messages.error(request, f" {msg}: {form.error_messages[msg]}")
            return render(request,"PaginaDePruebaApp/registro.html", {"form": form})
    else:
        form = ChoferRegisterForm()
        return render(request,"PaginaDePruebaApp/registro.html", {"form": form})

def Perfil(request):
    cliente=Cliente.objects.get(user_id=request.user.id)
    usuario = User.objects.filter(id= request.user.id).first()
    if request.method == "POST":
        form = EditarForm(request.POST, instance= usuario)
        form2 = EditarDniForm(request.POST, instance = cliente)
        if form.is_valid():
            if form2.is_valid():
                diccionario=form2.cleaned_data
                if diccionario["dni"] >= 0:
                    form.save()
                    form2.save()
                    return render(request,"PaginaDePruebaApp/perfil.html", {"form": form,"persona":cliente,"form2":form2,"cliente":cliente})
                else:
                    msg ="El dni debe ser un numero positivo"    ## Mensaje de error
                    form2.add_error("dni", msg)
                    return render(request,"PaginaDePruebaApp/perfil.html", {"form": form,"persona":cliente,"form2":form2,"cliente":cliente})
            else:
                return render(request,"PaginaDePruebaApp/perfil.html", {"form": form,"persona":cliente,"form2":form2,"cliente":cliente}) 
        else:
            return render(request,"PaginaDePruebaApp/perfil.html", {"form": form,"persona":cliente,"form2":form2,"cliente":cliente})
    else:
        form = EditarForm(instance = usuario)
        form2 = EditarDniForm(instance = cliente)
        return render(request, "PaginaDepruebaApp/perfil.html", {"form": form, "persona":cliente,"form2":form2,"cliente":cliente})

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
        msg ="INGRESE DATOS PARA SU BUSQUEDA."
        return render(request,"PaginaDePruebaApp/inicio.html", {"msg":msg}) 

def ResumenCompra(request,context):
    return render(request,"PaginaDePruebaApp/mensajeExitoCompra.html",context)

def CompraView(request,viaje_id):

    #Traigo el viaje y el usuario
    viaje=Viaje.objects.get(id=viaje_id)
    persona=Cliente.objects.get(user_id=request.user.id)

    #Me quedo con la lista de insumos del viaje
    insumosViaje=getInsumosViaje(viaje_id)

    #Si ya hay una compra la trae de la bd, sino la crea
    try:
        compra=Compra.objects.get(user_id=request.user.id,viaje_id=viaje_id)
    except :
        compra=Compra.objects.create(total=viaje.precio,viaje=viaje,user=persona)

    if compra.pendiente:
        return render(request,"PaginaDePruebaApp/mensajeCompraFallida.html")
    
    #Me quedo con la lista de invitados de la compra
    invitadosCompra=getInvitadosCompra(compra.id)

    #Me quedo con la lista de insumos de la compra
    insumosCompra=getInsumosCompra(compra.id)

    insumosCompraConCantidad=getInsumosConCantidad(insumosCompra,compra)

    if request.method == "POST":
        formTarjeta= TarjetaForm(request.user, request.POST,prefix="formTarjeta")
        if formTarjeta.is_valid():
            diccionario=formTarjeta.cleaned_data
            if chequearVencimiento(diccionario["fechaVto"]): 
                #calcula la cantidad de pasajes de la compra  
                cantPasajes=len(invitadosCompra)+1
                #si hay asientos disponibles, calcula el precio total (en caso de ser gold aplica descuento) y realiza la compra
                if viaje.asientosDisponibles >=cantPasajes:
                    compra.pendiente=True
                    compra.cancelado=False
                    #aplica descuento si es gold
                    if persona.esGold:
                        pasajeConDescuento=aplicarDescuento(viaje.precio)
                        compra.total=pasajeConDescuento*cantPasajes
                    else:
                        compra.total=viaje.precio*cantPasajes
                    compra.total=compra.total+calcularPrecioInsumos(insumosCompraConCantidad)
                    compra.save()
                    viaje.asientosDisponibles=viaje.asientosDisponibles-(len(invitadosCompra)+1)
                    viaje.save()
                    return render(request,"PaginaDePruebaApp/mensajeExitoCompra.html",{"compra":compra,"viaje":viaje,"invitados":invitadosCompra,"insumosCompraConCantidad":insumosCompraConCantidad})
                else:
                    msg ="No hay suficientes asientos disponibles"   ## Mensaje de error si esta vencida la tarjeta
                    formTarjeta.add_error("nro", msg)
                    return render(request,"PaginaDePruebaApp/compra.html", {"formTarjeta": formTarjeta , "viaje":viaje,"insumosViaje":insumosViaje,"insumosCompra":insumosCompra,"insumosCompraConCantidad":insumosCompraConCantidad,"persona":persona,"invitados":invitadosCompra})
            else:
                msg ="La tarjeta se encuentra vencida"   ## Mensaje de error si esta vencida la tarjeta
                formTarjeta.add_error("fechaVto", msg)
    else:
        if persona.esGold:
            formTarjeta = TarjetaForm(request.user, instance=persona.tarjeta, prefix="formTarjeta")
        else:
            formTarjeta = TarjetaForm(request.user,prefix="formTarjeta")
    return render(request,"PaginaDePruebaApp/compra.html", {"formTarjeta": formTarjeta , "viaje":viaje,"insumosViaje":insumosViaje,"insumosCompra":insumosCompra,"insumosCompraConCantidad":insumosCompraConCantidad,"persona":persona,"invitados":invitadosCompra})
            
def RegistroInvitado(request,viaje_id):

    #Traigo el viaje 
    viaje=Viaje.objects.get(id=viaje_id)

#info que necesito para implementar los invitados
    #Me traigo la compra actual
    compra=Compra.objects.get(viaje_id=viaje.id, user_id=request.user.id)

    #Me quedo con la lista de invitados de la compra

    invitadosCompra=getInvitadosCompra(compra.id)

    invitadosViajeDNI=getInvitadosViaje(viaje.id)

    #creo una lista de los dni de los invitados 
    invitadosCompraDNI=list(invitado.dni for invitado in invitadosCompra)

    if request.method== "POST":
        formInvitado=InvitadoForm(request.POST)
        if formInvitado.is_valid():
            invitadoInfo=formInvitado.cleaned_data
            #chequeo que el dni del invitado no esté ya registrado para la compra
            if not invitadoInfo['dni'] in invitadosCompraDNI:
                if not invitadoInfo['dni'] in invitadosViajeDNI:
                    #creo al invitado y a la relacion de la compra con el invitado
                    invitadoExisteQuery=Invitado.objects.filter(dni=invitadoInfo['dni'])
                    if not invitadoExisteQuery:
                        invitadoInfo=formInvitado.save()
                    else:
                        invitadoInfo=Invitado.objects.get(dni=invitadoInfo['dni'])
                    Compra.invitados.through.objects.create(compra_id=compra.id,invitado_id=invitadoInfo.id)
                    return redirect(CompraView,viaje_id=viaje.id)
                else:
                    msg ="El dni ingresado ya se encuentra registrado en la lista de pasajeros de este viaje"   ## Mensaje de error si ya se registro a un invitado con ese dni
                    formInvitado.add_error("dni", msg)
                    return render(request,"PaginaDePruebaApp/registroInvitado.html", {"formInvitado": formInvitado,"viaje":viaje})                
            else:
                msg ="El dni ingresado ya se encuentra registrado en la lista de invitados de esta compra"   ## Mensaje de error si ya se registro a un invitado con ese dni
                formInvitado.add_error("dni", msg)
                return render(request,"PaginaDePruebaApp/registroInvitado.html", {"formInvitado": formInvitado,"viaje":viaje})                
        else:
            return render(request,"PaginaDePruebaApp/registroInvitado.html", {"formInvitado": formInvitado,"viaje":viaje})
    else:
        formInvitado=InvitadoForm(request.POST)
        return render(request,"PaginaDePruebaApp/registroInvitado.html", {"formInvitado": formInvitado,"viaje":viaje})

def EliminarInvitado(request,invitado_id,viaje_id):
    #Me traigo la compra actual
    compra=Compra.objects.get(viaje_id=viaje_id, user_id=request.user.id)
    
    invitado=Invitado.objects.get(id=invitado_id)
    compraInvitado=Compra.invitados.through.objects.get(invitado_id=invitado.id,compra_id=compra.id)
    invitado.delete()
    compraInvitado.delete()
    return redirect(CompraView,viaje_id=viaje_id)
    
def EliminarInsumo(request,nombreInsumo,viaje_id):    
    #Me traigo la compra actual
    compra=Compra.objects.get(viaje_id=viaje_id, user_id=request.user.id)

    insumo=Insumo.objects.get(pk=nombreInsumo)
    compraInsumo=Compra.insumos.through.objects.get(insumo_id=insumo.nombre,compra_id=compra.id)
    insumoCompra=CantidadInsumo.objects.get(compra=compra,insumo=insumo)
    if insumoCompra.cantidad>1:
        insumo.stock=insumo.stock+1
        insumoCompra.cantidad=insumoCompra.cantidad-1
        insumoCompra.save()
    else:
        insumo.stock=insumo.stock+1
        compraInsumo.delete()
    insumo.save()
    
    return redirect(CompraView,viaje_id=viaje_id)
    

def AgregarInsumo(request,nombreInsumo,viaje_id):
    #Me traigo la compra actual
    compra=Compra.objects.get(viaje_id=viaje_id, user_id=request.user.id)

    insumo=Insumo.objects.get(pk=nombreInsumo)
    insumo.stock=insumo.stock-1
    insumo.save()

    try:
        insumoCompra=CantidadInsumo.objects.get(compra=compra,insumo=insumo)
    except:
        compra.insumos.add(insumo,through_defaults={'cantidad':1})
        return redirect(CompraView,viaje_id=viaje_id)
    
    insumoCompra.cantidad=insumoCompra.cantidad+1
    insumoCompra.save()

    return redirect(CompraView,viaje_id=viaje_id)
    

def CancelarPasaje(request, id_viaje):
    compras = Compra.objects.filter(viaje__id__icontains=id_viaje, user__user__id__icontains=request.user.id)
    for compra in compras:
        if compra.pendiente:
            dinero=compra.total
            invitadosCompra=getInvitadosCompra(compra.id)
            viaje=compra.viaje
            viaje.asientosDisponibles=(compra.viaje.asientosDisponibles) + 1 + len(invitadosCompra)
            viaje.save()
            compra.cancelado=True
            compra.pendiente=False
            compra.save()
            return render (request, "PaginaDePruebaApp/cancelarPasaje.html", {"dinero": dinero})

