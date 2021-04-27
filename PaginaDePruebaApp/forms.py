from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
    nombre_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su nombre")', 'oninput': 'this.setCustomValidity("")'}
    apellido_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su apellido")', 'oninput': 'this.setCustomValidity("")'}
    user_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese un nombre de usuario")', 'oninput': 'this.setCustomValidity("")'}
    dni_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su DNI")', 'oninput': 'this.setCustomValidity("")'}
    contra_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese una contraseña")', 'oninput': 'this.setCustomValidity("")'}
    first_name= forms.CharField(label='Nombre', max_length=30,widget=forms.TextInput(attrs=nombre_attr))
    last_name= forms.CharField(label='Apellido',max_length=30,widget=forms.TextInput(attrs=apellido_attr))
    username = forms.CharField(label='Nombre de usuario',max_length=20,widget=forms.TextInput(attrs=user_attr))
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget= forms.PasswordInput(attrs=contra_attr))
    password2 = forms.CharField(label='Confirmar contraseña',widget= forms.PasswordInput(attrs=contra_attr))
    dni = forms.IntegerField(label='DNI', max_value=99999999,widget=forms.TextInput(attrs=dni_attr))
    fechaDeNacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.SelectDateWidget(years=range(1920, 2100)))
    class Meta:
        model = get_user_model()
        fields= ['first_name','last_name','username','email','password1','password2','dni','fechaDeNacimiento']
        help_text = {k:"" for k in fields }
       

