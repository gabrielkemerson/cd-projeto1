from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from time import sleep


# a classe deveria ser movida pra um arquivo separado, porém por conta de um erro ela permanecerá aqui # noqa
class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        sleep(seconds)

    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        element = self.browser.find_element(By.XPATH, '/html/body/main/div/div') # noqa
        self.assertIn('Não temos nenhuma receita publicada 🥲', element.text)
