from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils import django_forms


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aqui é ultilizado a função para adicionar um texto ao placeholder

        django_forms.add_placeholder(self.fields['last_name'], 'Sobre nome')

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
        help_text='No mínimo 8 caracteres, Letras maiusculas minusculas e números.',
        validators=[django_forms.strong_password],
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

    # Validação de campos independentes
    # Quando você usa um clean_nomedocampo ele é automaticamente lincado ao campoexistente sem que você precise fazer nenhum outro prossedimento para isso # noqa
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            # Não precisamos especificar a qual campo o erro será atribuido, porque essa atribuição é feita no nome da função já que é um tratamento de campo independente # noqa
            raise ValidationError(
                'Este e-mail já está em uso',
                code='invalid',
            )
        # Lembre-se de retornar o campo para que os erros do mesmo sejam exibidos nos testes # noqa
        return email
    
    # Validação de campos dependentes
    def clean(self):
        # nesta variável é passado todos os valores dos campos das variáveis
        # poderiam ser passados da seguinte forma cleaned_data = self.cleaned_data.get() porém a documentação do Django recomenda que façamos como descrito a baixo # noqa
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            # Aqui precisamos especificar em qual campo será exibido o erro porque a atribuição do tratamento não é feita no nome da função # noqa
            raise ValidationError({
                'password': 'As senhas são divergentes',
                'password2': 'As senhas são divergentes'})
