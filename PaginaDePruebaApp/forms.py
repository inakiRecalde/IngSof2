from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Cliente, User
from django.contrib.auth import authenticate

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

    #con esto estaba intentando armar los diferentes usuarios pero si sacas el username del formulario se rompe todo
    def save(self):
      user=super().save(commit=False)
      user.esCliente=True
      user.username=self.cleaned_data.get('email')
      user.save()
      cliente=Cliente.objects.create(user=user)
      cliente.dni=self.cleaned_data.get('dni')
      cliente.save()
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
    """def __init__(self, *args, **kwargs):
      
        super(LoginForm(), self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})"""

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Email o contraseña invalidos')


#esto era para configurar desde panel de admin pero no se
class CrearChoferForm(forms.ModelForm):
    email=forms.EmailField(label="Email")
    def clean_name(self):
        self.clean()
        # do something that validates your data
        return self.cleaned_data["email"]

