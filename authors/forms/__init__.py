# Quando colocamos esta importação neste arquivo __init__.py ela é disponibilizada
# assim que importamos o "pacote forms" então ao invéz de importar-mos o modulo RegisterForm
# from authors.forms.register_form import RegisterForm
# Podemos importar direto from authors.forms import RegisterForm. Pois como a importação é declarada
# neste arquivo, assim que usamos o pacote forms esta importação já virá automaticamente com ele
from . register_form import RegisterForm
from . login import LoginForm