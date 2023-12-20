from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


# Nesta função receberemos um campo, o widget que será alterado e o novo valor deste widget # noqa
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# esta função recebe um campo e uma string pare redefinir o placeholder
# Neste caso não re reescrevemos um field, apenas adicionamos imformações a ele
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


# Função para validação através de validators
def strong_password(password):
    # aqui será checado se existem letras de a-z minusculas, letras de A-Z maiusculas, números de 1-9 e se tem no mínimo 8 caracteres # noqa
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    # Se a senha não corresponder aos requisitos
    if not regex.match(password):

        raise ValidationError((
            'Sua senha deve conter '
            'no mínimo 8 caracteres '
            'letras maiusculas minúsculas e números'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aqui é ultilizado a função para adicionar um texto ao placeholder

        add_placeholder(self.fields['last_name'], 'Sobre nome')

    # Sub-escrições
    # aqui estão sendo feitas a bonescrição dos campos, ou seja é como se eles estivessem sendo refeitos e reconfigurados. É aconselhado fazer esse tipo de mudança de um só jeito para evitar bugs ou confusão de placeholder por exemplo # noqa
    first_name = forms.CharField(

        widget=forms.TextInput(attrs={
            'placeholder': 'Primeiro nome'
        }),
        error_messages={
            'required': '* Este campo não pode ser vazio'
        },
        label='First name'
    )

    last_name = forms.CharField(
        required=True,
        error_messages={
            'required': '* Este campo não pode ser vazio'
        },
        label='Last name'
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário'
        }),
        help_text='Obrigatório, letras, números e  @.+-_. apenas.', # noqa
        error_messages={
            'required': '* Este campo é obrigatório',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
    )

    email = forms.EmailField(
        error_messages={'required': '* O campo de E-mail é obrigatório'},
        label='E-mail',
        help_text='Digite um e-mail válido',
        widget=forms.TextInput(attrs={
            'placeholder': 'E-mail'
        }),
    )

    password = forms.CharField(

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        }),
        error_messages={
            'required': '* Este campo é obrigatório'
        },
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        }),

        error_messages={
            'required': '* Este campo é obrigatório'
        },
        label='Password2'
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

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Primeiro nome'
                }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Senha'
            })
        }

    # Validação de campos dependentes
    def clean(self):
        # nesta variável é passado todos os valores dos campos das variáveis
        # poderiam ser passados da seguinte forma cleaned_data = self.cleaned_data.get() porém a documentação do Django recomenda que façamos como descrito a baixo # noqa
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:

            raise ValidationError({
                'password': 'As senhas são divergentes',
                'password2': 'As senhas são divergentes'})
