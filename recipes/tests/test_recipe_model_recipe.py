from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


# esta classe foi feita para testar os models do app recipes
class RecipeModelTest(RecipeTestBase):
    # Como ja informado em outras classes o setUp é feito
    # para ser executado automaticamente antes de todos os testes
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    # Aqui é usado o parameterized para Fazer um sub grupo de testes dentro do teste    # noqa
    # Os parametros devem ser passados no modelo a baixo, com uma lista de tuplas   # noqa
    @parameterized.expand([
        ('title', 65),
        ('description', 200),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    # Na função a baixo são definidos os dois campos que irão representar cada elemento da tupla que serão "field" e "max_length" respectivamente   # noqa
    def test_recipe_fields_max_length(self, field, max_length):
        # Aqui é usado o setattr() para passar valores para objeto já criado pela função setUp o titulo recebe propositalmente uma quantidade de caracteres além da quantidade permitida para que um erro seja levantado    # noqa
        setattr(self.recipe, field, 'A' * (max_length + 1))

        # Aqui é feita uma asserção afirmando que um erro de validação será levantado    # noqa
        with self.assertRaises(ValidationError):
            # Aqui é feito a checagem através do full_clean() para que o erro seja levantado já que infelizmente o Django não faz a validação poir padrão   # noqa
            self.recipe.full_clean()
