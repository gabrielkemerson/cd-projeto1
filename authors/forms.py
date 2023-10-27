from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Nesta função receberemos um campo, o widget que será alterado e o novo valor deste widget # noqa
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# esta função recebe um campo e uma string pare redefinir o placeholder
# Neste caso não re reescrevemos um field, apenas adicionamos imformações a ele
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


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
            'required': '*obrigatório',
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

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:

            raise ValidationError(
                'Não digite %(value)s na sua senha!',
                code='invalid',
                params={'value': '"Atenção"'}
            )

        return data

    def clean_username(self):
        data = self.cleaned_data.get('username').lower()

        if 'robertinho' in data:

            raise ValidationError(
                'Seu nome de usuário não pode conter %(value)s',
                code='invalid',
                params={'value': '"Robertinho"'}
            )

        return data

    def clean(self):
        # nesta variável é passado todos os valores dos campos das variáveis
        # poderiam ser passados da seguinte forma cleaned_data = self.cleaned_data.get() porém a documentação do Django recomenda que façamos como descrito a baixo # noqa
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:

            raise ValidationError({
                'password': f'As senhas são divergentes "{password}"',
                'password2': f'As senhas são divergentes "{password2}"'})
