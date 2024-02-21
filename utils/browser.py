from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from time import sleep


ROOT_PATH = Path(__file__).parent.parent


# O código está em uma função para não fica executando automaticamente
def make_chrome_browser(*options):
    # Cria um objeto com as opções
    chrome_options = webdriver.ChromeOptions()
    # um if para ver se a tupla *options tem argumentos
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    # Cria um objeto de serviço. Os parametros dentro dele passados são padrão
    servico = Service(ChromeDriverManager().install())
    # Cria um objeto de navegador que recebe os parametros de serviço e opções
    navegador = webdriver.Chrome(service=servico, options=chrome_options)
    return navegador


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('https://chat.openai.com/c/69e30858-dc41-495d-948a-329d7dda6e8b')
    sleep(5)
