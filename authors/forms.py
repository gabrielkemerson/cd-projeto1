from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        help_texts = {
            'email': 'Digite um e-mail válido'
        }

        error_messages = {
            'username': {
                'required': 'Este campo não pode ser vazio!'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Primeiro nome'
                }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Senha'
            })
        }
