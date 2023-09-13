# O testCase já é importado por padrão no test.py do app
from django.test import TestCase
# O reverse retorna a URL apartir de uma view
# Já a função resolve serve para testar se uma URL específica está associada à visualização correta    # noqa
from django.urls import reverse, resolve
# Lembre-se sempre de importar as views para testa-las
from recipes import views
# Importa os models de recipe junto com o User (lembre-se de que se o import do User for removido de models ele quebrara o teste)    # noqa
from recipes.models import Category, Recipe, User

# Esta é a classe que contem todos os testes deste arquivo
class RecipeViewsTest(TestCase):    # noqa
    # Lembre-se de sempre de começar o nome dos seus testes com a palavra "test" e escreva o nome dos testes de maneira bem detalhada, não importa se eles vão ficar muito grandes, o importante é ser bem descritivo    # noqa
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        # Quando for usar o reverse, lembre-se de que, se a url que você está passando recebe algum parâmetro você deve passar este parâmetro. Neste caso usamos o "kwargs" para isso    # noqa
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    # A função client simula uma requisição feita por um usuário e retorna diversas informações desta requisição como doc HTML, Template, Status code, entre muitas outras informações    # noqa

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEquals(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1> Não temos nenhuma receita publicada 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Test category')    # noqa
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )

        recipe = Recipe.objects.create(    # noqa
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertIn(author.first_name, content)
        self.assertIn(category.name, content)
        self.assertEquals(len(response_context_recipes), 1)
        pass
