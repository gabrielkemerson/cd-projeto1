from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


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
