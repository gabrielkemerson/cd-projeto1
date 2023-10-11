# O reverse retorna a URL apartir de uma view
# Já a função resolve serve para testar se uma URL específica está associada à visualização correta    # noqa
from django.urls import reverse, resolve
# Lembre-se sempre de importar as views para testa-las
from recipes import views
# Importa os models de recipe junto com o User (lembre-se de que se o import do User for removido de models ele quebrara o teste)    # noqa
# from recipes.models import Category, Recipe, User
from .test_recipe_base import RecipeTestBase

# Esta é a classe que contem todos os testes deste arquivo
class RecipeSearchViewTest(RecipeTestBase):    # noqa
    # Lembre-se de sempre de começar o nome dos seus testes com a palavra "test" e escreva o nome dos testes de maneira bem detalhada, não importa se eles vão ficar muito grandes, o importante é ser bem descritivo    # noqa

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=valor'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)

        self.assertIn(
            'Search for &lt;Teste&gt; | Recipe',
            response.content.decode('utf-8')
        )

    # Não faz parte do curso
    def test_recipe_published_is_find_in_search_page(self):
        receita = self.make_recipe(is_published=True)
        url = reverse('recipes:search') + f'?q={receita.title}'
        response = self.client.get(url)

        self.assertIn(
            f'{receita.preparation_time} {receita.preparation_time_unit}',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is title one'
        title2 = 'This is title two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'}
        )

        response1 = self.client.get(reverse('recipes:search') + f'?q={title1}')
        response2 = self.client.get(reverse('recipes:search') + f'?q={title2}')
        response_both = self.client.get(reverse('recipes:search') + '?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
