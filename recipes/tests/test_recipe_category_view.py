# O reverse retorna a URL apartir de uma view
# Já a função resolve serve para testar se uma URL específica está associada à visualização correta    # noqa
from django.urls import reverse, resolve
# Lembre-se sempre de importar as views para testa-las
from recipes import views
# Importa os models de recipe junto com o User (lembre-se de que se o import do User for removido de models ele quebrara o teste)    # noqa
# from recipes.models import Category, Recipe, User
from .test_recipe_base import RecipeTestBase

# Esta é a classe que contem todos os testes deste arquivo
class RecipeCategoryViewTest(RecipeTestBase):    # noqa
    # Lembre-se de sempre de começar o nome dos seus testes com a palavra "test" e escreva o nome dos testes de maneira bem detalhada, não importa se eles vão ficar muito grandes, o importante é ser bem descritivo    # noqa

    def test_recipe_category_view_function_is_correct(self):
        # Quando for usar o reverse, lembre-se de que, se a url que você está passando recebe algum parâmetro você deve passar este parâmetro. Neste caso usamos o "kwargs" para isso    # noqa
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'This is a category test'
        self.make_recipe(title=title)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(

            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id}
            )
        )

        self.assertAlmostEqual(response.status_code, 404)
