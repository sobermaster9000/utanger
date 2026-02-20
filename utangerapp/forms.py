from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)