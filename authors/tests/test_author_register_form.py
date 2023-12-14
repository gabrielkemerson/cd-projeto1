from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('username', 'Nome de usuário'),
        ('email', 'E-mail'),
        ('password', 'Digite sua senha'),
        ('password2', 'Confirme sua senha'),
        ('last_name', 'Sobre nome'),
    ])
    def test_fields_placeholder(self, field, placeholder):

        form = RegisterForm()

        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('email', 'Digite um e-mail válido'),
        ('username', 'Obrigatório, letras, números e  @.+-_. apenas.')
    ])
    def test_fields_help_text(self, field, needed):

        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):

        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):

    def setUp(self, *args, **kwargs):

        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', '* Este campo é obrigatório'),
        ('first_name', '* Este campo não pode ser vazio'),
        ('last_name', '* Este campo não pode ser vazio'),
        ('password', '* Este campo é obrigatório'),
        ('password2', '* Este campo é obrigatório'),
        ('email', '* O campo de E-mail é obrigatório')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        url = reverse('authors:create')
        # Este folow é usado pe neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data[field] = ''
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
