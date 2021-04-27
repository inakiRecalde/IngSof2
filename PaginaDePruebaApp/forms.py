from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
    first_name= forms.CharField(label='Nombre')
    last_name= forms.CharField(label='Apellido')
    username = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField()
    password1 = forms.CharField(label='password',widget= forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar password',widget= forms.PasswordInput)
    dni = forms.IntegerField(label='dni')
    fechaDeNacimiento = forms.DateField(label='fecha de nacimiento')
    class Meta:
        model = get_user_model()
        fields= ['first_name','last_name','username','email','password1','password2','dni','fechaDeNacimiento']
        help_text = {k:"" for k in fields }

