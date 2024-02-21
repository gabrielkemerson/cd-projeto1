from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from time import sleep


class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):

    def sleep(self, seconds=5):
        sleep(seconds)

    def testthetest(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        self.sleep()
        element = browser.find_element(By.XPATH, '/html/body/main/div/div')
        self.assertIn('Não temos nenhuma receita publicada 🥲', element.text)
