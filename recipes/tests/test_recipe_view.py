# O testCase já é importado por padrão no test.py do app
from django.test import TestCase
# O reverse retorna a URL apartir de uma view
# Já a função resolve serve para testar se uma URL específica está associada à visualização correta    # noqa
from django.urls import reverse, resolve
# Lembre-se sempre de importar as views para testa-las
from recipes import views


# Esta é a classe que contem todos os testes deste arquivo
class RecipeViewsTest(TestCase):
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
