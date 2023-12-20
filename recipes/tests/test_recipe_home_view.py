# O reverse retorna a URL apartir de uma view
# Já a função resolve serve para testar se uma URL específica está associada à visualização correta    # noqa
from django.urls import reverse, resolve
# Lembre-se sempre de importar as views para testa-las
from recipes import views
# Importa os models de recipe junto com o User (lembre-se de que se o import do User for removido de models ele quebrara o teste)    # noqa
# from recipes.models import Category, Recipe, User
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch

# Esta é a classe que contem todos os testes deste arquivo
class RecipeHomeViewTest(RecipeTestBase):    # noqa
    # Lembre-se de sempre de começar o nome dos seus testes com a palavra "test" e escreva o nome dos testes de maneira bem detalhada, não importa se eles vão ficar muito grandes, o importante é ser bem descritivo    # noqa

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    # A função client simula uma requisição feita por um usuário e retorna diversas informações desta requisição como doc HTML, Template, Status code, entre muitas outras informações    # noqa

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1> Não temos nenhuma receita publicada 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1> Não temos nenhuma receita publicada 🥲</h1>',
            response.content.decode('utf-8')
        )
        self.assertEqual(
            len(response.context['recipes']), 0
        )

    def test_recipe_home_is_paginated(self):

        for con in range(8):
            kwargs = {
                'author_data': {'username': f'a{con}'},
                'slug': f's{con}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGES', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertAlmostEqual(paginator.num_pages, 3)
            self.assertAlmostEqual(len(paginator.get_page(1)), 3)
            self.assertAlmostEqual(len(paginator.get_page(2)), 3)
            self.assertAlmostEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):

        for con in range(8):
            kwargs = {
                'author_data': {'username': f'a{con}'},
                'slug': f's{con}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGES', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')

            self.assertEqual(
                response.context['recipes'].number,
                1
            )

            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )

            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
            