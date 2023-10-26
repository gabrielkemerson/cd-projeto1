from django import forms
from django.contrib.auth.models import User


# esta função recebe um campo e uma string pare redefinir o placeholder
# Neste caso não re reescrevemos um field, apenas adicionamos imformações a ele
def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aqui é ultilizado a função para adicionar um texto ao placeholder
        add_placeholder(self.fields['last_name'], 'Sobre nome')

    # Sub-escrições
    first_name = forms.CharField(
        required=False,

        widget=forms.TextInput(attrs={
            'placeholder': 'Primeiro nome'
        }))

    username = forms.CharField(
        required=True,

        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário'
        }),
        error_messages={
            'required': '* Obrigatório'
        }
    )

    email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'E-mail'
    }))

    password = forms.CharField(
        required=True,

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        }),
        error_messages={
            'required': '* Obrigatório'
        }
    )

    password2 = forms.CharField(
        required=True,

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        }),
        error_messages={
            'required': '* Obrigatório'
        }
    )

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

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Primeiro nome'
                }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Senha'
            })
        }
