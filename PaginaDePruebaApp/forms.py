from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Cliente

class UserRegisterForm(UserCreationForm):
    #mensajes de error
    nombre_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su nombre")', 'oninput': 'this.setCustomValidity("")'}
    apellido_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su apellido")', 'oninput': 'this.setCustomValidity("")'}
    user_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese un nombre de usuario")', 'oninput': 'this.setCustomValidity("")'}
    dni_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese su DNI")', 'oninput': 'this.setCustomValidity("")'}
    contra_attr = {'oninvalid': 'this.setCustomValidity("Por favor ingrese una contraseña")', 'oninput': 'this.setCustomValidity("")'}

    #campos del formulario
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

    #con esto estaba intentando armar los diferentes usuarios pero si sacas el username del formulario se rompe todo
    def save(self):
      user=super().save(commit=False)
      user.esCliente=True
      print(self.cleaned_data)
      user.username=self.cleaned_data.get('email')
      user.save()
      cliente=Cliente.objects.create(user=user)
      cliente.dni=self.cleaned_data.get('dni')
      cliente.save()
      return user

class LoginForm(forms.Form):
    email=forms.EmailField(label="Email")
    contrasenia= forms.CharField(label='Contraseña',widget=forms.PasswordInput())


#esto era para configurar desde panel de admin pero no se
class CrearChoferForm(forms.ModelForm):
    email=forms.EmailField(label="Email")
    def clean_name(self):
        # do something that validates your data
        return self.cleaned_data["email"]

