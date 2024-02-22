from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from time import sleep


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        sleep(seconds)

    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
