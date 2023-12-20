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
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data[field] = ''
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        url = reverse('authors:create')
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data['username'] = 'Noa'
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        url = reverse('authors:create')
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data['username'] = 'G' * 151
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        url = reverse('authors:create')
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data['password'] = 'abc123'
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Sua senha deve conter '
            'no mínimo 8 caracteres '
            'letras maiusculas minúsculas e números'
        )
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        url = reverse('authors:create')
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data['password'] = 'AAabc123'
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        url = reverse('authors:create')
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data['password'] = 'AAabc123'
        self.form_data['password2'] = 'BBabc123'
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas são divergentes'
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        url = reverse('authors:create')
        # Este folow é usado porque neste teste em específico a página tem que ser redirecionada para uma outra view # noqa
        self.form_data['password'] = 'AAabc123'
        self.form_data['password2'] = 'AAabc123'
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
