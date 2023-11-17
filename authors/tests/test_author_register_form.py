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
    def test_first_name_placeholder_is_correct(self, field, placeholder):

        form = RegisterForm()

        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)
