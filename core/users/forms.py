from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.users.models import CustomUser


class RegisterForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password'
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
