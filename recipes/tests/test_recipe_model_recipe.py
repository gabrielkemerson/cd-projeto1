from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


# esta classe foi feita para testar os models do app recipes
class RecipeModelTest(RecipeTestBase):
    # Como ja informado em outras classes o setUp é feito
    # para ser executado automaticamente antes de todos os testes
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    # Aqui é testado se o djando realmente está validando a quantidade
    # de caracteres do titulo
    def test_recipe_title_rises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70
        # Criamos um bloco com with e nele fazemos uma asserção afirmando
        # que o Django irá levantar um erro de validação
        with self.assertRaises(ValidationError):
            # Infelizmente o Django não faz a validação por padrão
            # por isso temos que usar o "full_clean()" para garantir
            # que o Django valide as informações de acordo com os padrões
            # dos Models criados
            self.recipe.full_clean()

    def test_recipe_fields_max_length(self):

        fields = [
            ('title', 65),
            ('description', 200),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]

        for field, max_length in fields:
            setattr(self.recipe, field, 'A' * (max_length + 1))

            with self.assertRaises(ValidationError):
                self.recipe.full_clean()
