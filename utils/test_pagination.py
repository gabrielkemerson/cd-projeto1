# esta é uma função que apesar de trabalhar em conjunto com o django ela não é uma função exclusiva do django então por isso não usaremos o django.test, ao invés disso usaremos o unittest que é do próprio python e faz parte do python por padrão e não do django. Mas lembre-se caso deixe de usar o django.test você irá perder algumas acerssões, e ficará apenas com as acerssões "cruas do python" digamos assim    # noqa
from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pass
