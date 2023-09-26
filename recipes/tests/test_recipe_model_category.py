from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


# esta classe foi feita para testar os models do app recipes
class CategoryModelTest(RecipeTestBase):
    # Como ja informado em outras classes o setUp é feito
    # para ser executado automaticamente antes de todos os testes
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Testing category'
        )
        return super().setUp()

    def test_recipe_category_model_string_representarion_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()
