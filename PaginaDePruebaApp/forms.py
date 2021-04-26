from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='password',widget= forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar password',widget= forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields= ['username','email','password1','password2']
        help_text = {k:"" for k in fields }

