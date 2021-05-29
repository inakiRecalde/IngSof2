
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import widgets
from django.forms import fields
from .models import Cliente, Comentario, Compra, Invitado, Tarjeta, User,Chofer,Insumo,Viaje
from django.forms.fields import Field
from django.contrib.auth import authenticate
from django.forms.models import ModelMultipleChoiceField

class UserRegisterForm(UserCreationForm):
    #mensajes de error
    nombre_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su nombre")', 'oninput': 'this.setCustomValidity("")'}
    apellido_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su apellido")', 'oninput': 'this.setCustomValidity("")'}
    dni_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su DNI")', 'oninput': 'this.setCustomValidity("")'}
    contra_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese una contraseña")', 'oninput': 'this.setCustomValidity("")'}

    #campos del formulario
    first_name= forms.CharField(label='Nombre', max_length=30,widget=forms.TextInput(attrs=nombre_attr))
    last_name= forms.CharField(label='Apellido',max_length=30,widget=forms.TextInput(attrs=apellido_attr))
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget= forms.PasswordInput(attrs=contra_attr))
    password2 = forms.CharField(label='Confirmar contraseña',widget= forms.PasswordInput(attrs=contra_attr))
    dni = forms.IntegerField(label='DNI', max_value=99999999,widget=forms.TextInput(attrs=dni_attr))
    fechaDeNacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.SelectDateWidget(years=range(1920, 2100)))

    class Meta:
        model = get_user_model()
        fields= ['first_name','last_name', 'email','password1','password2','dni','fechaDeNacimiento']
        help_text = {k:"" for k in fields }

    def save(self):
      user=super().save(commit=False)
      user.esCliente=True
      user.username=self.cleaned_data.get('email')
      user.save()
      cliente=Cliente.objects.create(user=user)
      cliente.dni=self.cleaned_data.get('dni')
      cliente.save()
      return user

class ChoferRegisterForm(UserCreationForm):
    #mensajes de error
    nombre_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su nombre")', 'oninput': 'this.setCustomValidity("")'}
    apellido_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su apellido")', 'oninput': 'this.setCustomValidity("")'}
    tel_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese un numero de telefono")', 'oninput': 'this.setCustomValidity("")'}
    contra_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese una contraseña")', 'oninput': 'this.setCustomValidity("")'}

    #campos del formulario
    first_name= forms.CharField(label='Nombre', max_length=30,widget=forms.TextInput(attrs=nombre_attr))
    last_name= forms.CharField(label='Apellido',max_length=30,widget=forms.TextInput(attrs=apellido_attr))
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget= forms.PasswordInput(attrs=contra_attr))
    password2 = forms.CharField(label='Confirmar contraseña',widget= forms.PasswordInput(attrs=contra_attr))
    tel = forms.IntegerField(label='Teléfono',widget=forms.TextInput(attrs=tel_attr), max_value=9999999999)

    class Meta:
        model = get_user_model()
        fields= ['first_name','last_name', 'email','password1','password2','tel']
        help_text = {k:"" for k in fields }

    def save(self):
      user=super().save(commit=False)
      user.esChofer=True
      user.username=self.cleaned_data.get('email')
      user.save()
      chofer=Chofer.objects.create(user=user)
      chofer.telefono=self.cleaned_data.get('tel')
      chofer.save()
      return user

class LoginForm(forms.ModelForm):
    email=forms.EmailField(label="Email")
    password  = forms.CharField(label= 'Contraseña', widget=forms.PasswordInput)

    class Meta:
        model  =  User
        fields =  ('email', 'password')
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'password':forms.TextInput(attrs={'class':'form-control'}),
        }
        help_text = {k:"" for k in fields }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Email o contraseña invalidos')

class ChoferAdminForm(forms.ModelForm):
    class Meta:
        widgets={'telefono': forms.TextInput(attrs={'size':15})}


class TarjetaForm(forms.ModelForm):
    nroTarjeta= forms.IntegerField(label="Número de tarjeta")
    fechaVto=forms.DateField(label='Fecha de vencimiento', widget=forms.SelectDateWidget(years=range(1990, 2100)))
    codigo=forms.IntegerField(label="Código")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TarjetaForm, self).__init__(*args, **kwargs)

    class Meta:
            model = Tarjeta
            fields= ['nroTarjeta', 'codigo']
            help_text = {k:"" for k in fields }

    def save(self):
        tarjeta=Tarjeta.objects.create(
            nro=self.cleaned_data.get('nroTarjeta'), 
            fechaVto=self.cleaned_data.get('fechaVto'),
            codigo=self.cleaned_data.get('codigo')
        )

        cliente=Cliente.objects.get(user_id=self.user.id)
        cliente.esGold=True
        cliente.tarjeta=tarjeta
        cliente.save()
        return tarjeta
        
class EditarDniForm(forms.ModelForm):
    dni = forms.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ['dni']

class EditarForm(forms.ModelForm):

    #campos del formulario
    first_name= forms.CharField(label='Nombre', max_length=30,widget=forms.TextInput())
    last_name= forms.CharField(label='Apellido',max_length=30,widget=forms.TextInput())
    email = forms.EmailField()
    
    class Meta:
        model = get_user_model()
        
        fields= ['first_name','last_name', 'email']

    def __init__(self ,*args, **kwargs):
        super(EditarForm, self).__init__(*args, **kwargs) 

class CambiarContraForm(forms.ModelForm):
    passwordActual = forms.CharField(label='Contraseña actual',widget= forms.PasswordInput())
    password1 = forms.CharField(label='Contraseña nueva',widget= forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar contraseña nueva',widget= forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields= ['passwordActual','password1','password2']


#formularios para la compra

class MyMultipleModelChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return "%s, precio: $%s" % (obj.nombre,obj.precio)

class CompraInsumosForm(forms.ModelForm):
    
    class Meta:
        model = Compra
        fields = (
            'insumos',
            )

    def __init__(self, *args, **kwargs):

        # call the parent init
        super(CompraInsumosForm, self).__init__(*args, **kwargs)
        viajeInsumosQuery=Viaje.insumo.through.objects.filter(viaje_id=self.instance.id)
        id_insumos=viajeInsumosQuery.values_list('insumo_id')
        
        self.fields['insumos'] = MyMultipleModelChoiceField(
            queryset=Insumo.objects.filter(pk__in=id_insumos), 
            required=False, 
            widget=forms.SelectMultiple()
            
            )

class InvitadoForm(forms.ModelForm):
    nombre_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su nombre")', 'oninput': 'this.setCustomValidity("")'}
    apellido_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su apellido")', 'oninput': 'this.setCustomValidity("")'}
    dni_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su DNI")', 'oninput': 'this.setCustomValidity("")'}

    nombre=forms.CharField(label='Nombre', max_length=30,widget=forms.TextInput(attrs=nombre_attr))
    apellido=forms.CharField(label='Apellido',max_length=30,widget=forms.TextInput(attrs=apellido_attr))
    dni = forms.IntegerField(label='DNI', max_value=99999999,widget=forms.TextInput(attrs=dni_attr))

    class Meta:
        model = Invitado
        fields = (
            'nombre','apellido','dni'
            )



#CHOICES = [('1', '★'), ('2', '★'),('3', '★'), ('4', '★'),('5', '★')]
class ComentInputForm(forms.ModelForm):
    texto_attr = {'oninvalid': 'this.setCustomValidity("Por favor un texto")', 'oninput': 'this.setCustomValidity("")'}   

    texto=forms.CharField(label='Ingrese un comentario', max_length=30,widget=forms.TextInput(attrs=texto_attr))
    #forms.ChoiceField(choices=CHOICES,type="radio",widget= forms.RadioSelect(attrs={'class' : 'Estrella'}))

    
    class Meta:
        model = Comentario  
        fields = (
            'texto',
        ) 

    def save(self):
        coment = Comentario.objects.create(
            texto=self.cleaned_data.get('texto'),
            puntuacion = '2'
        )
        return coment
          