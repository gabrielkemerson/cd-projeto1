# O reverse retorna a URL apartir de uma view
# Já a função resolve serve para testar se uma URL específica está associada à visualização correta    # noqa
from django.urls import reverse, resolve
# Lembre-se sempre de importar as views para testa-las
from recipes import views
# Importa os models de recipe junto com o User (lembre-se de que se o import do User for removido de models ele quebrara o teste)    # noqa
# from recipes.models import Category, Recipe, User
from .test_recipe_base import RecipeTestBase

# Esta é a classe que contem todos os testes deste arquivo
class RecipeDetailViewTest(RecipeTestBase):    # noqa
    # Lembre-se de sempre de começar o nome dos seus testes com a palavra "test" e escreva o nome dos testes de maneira bem detalhada, não importa se eles vão ficar muito grandes, o importante é ser bem descritivo    # noqa

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        title = 'This is a detail page test'
        self.make_recipe(title=title)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(

            reverse(
                'recipes:recipe',
                kwargs={'id': recipe.id}
            )
        )

        self.assertAlmostEqual(response.status_code, 404)
