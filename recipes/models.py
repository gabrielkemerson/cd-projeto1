# LEMBRE-SE !! após qualquer alteração ou criação você deve informarpro django que essa alteração foi feita para que ele possa deixar a sua base de dados igual ao seu código. Para isso crie a migração através do comando 'python manage.py makemigrations' e em seguida realize essas migrações para o banco de dados atravéz do comando 'python manage.py migrate'

from django.db import models
from django.contrib.auth.models import User

# Create your models here.  

class Category(models.Model):

    name = models.CharField(max_length=65)

    # Esta função serve para que o MODEL retorne seu nome ao inves do ID. Desta forma a sua identificação será bem mais facil na tela de ADMIN
    def __str__(self):
        titulo = str(self.id)
        titulo += f' - {self.name}'
        return titulo


class Recipe(models.Model): 

    # Cria uma coluna chamada 'title' que recebe um CharField(que é o equivalente ao VarChar no SQL) que pode receber no máximo 65 caracteres
    title = models.CharField(max_length=65)

    # Cria uma coluna chamada description que também recebe um Charfield de no máximo 200 caracteres
    description = models.CharField(max_length=200)

    # O slug é uma parte de uma URL que identifica de forma descritiva e amigável um recurso específico em um site
    slug = models.SlugField()

    # Cria uma coluna chamada preparation_time que recebe um IntegerField, que é um objeto que recebe valores Inteiros    
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)

    # Cria uma coluna que recebe um objeto de texto que é diferente de um input como um CharField por exemplo, e neste caso o TextField não tem limite de caracteres
    preparation_steps = models.TextField()

    # Cria uma coluna chamada 'preparation_steps_is_html que vai receber um objeto que recebe valores boleanos
    preparation_steps_is_html = models.BooleanField(default=False)

    # Cria uma coluna do tipo DATA e o parametro 'auto_now_add=True' faz com que esta coluna pegue a data atual e adicione neste campo automaticamente 
    created_at = models.DateTimeField(auto_now_add=True)

    # Cria uma coluna do tipo data que vai adicionar a data da ultima alteração, a diferença deste elemento para o elemento acima é que quando a receita for atualizada apenas esta data será alterada, diferente da data de criação
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    # Cria uma coluna que vai receber uma imagem. O parametro 'upload_to' recebe uma pasta e uma data que vai ser a data em que aquela imagem foi adicionada
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', blank=True, default='')

    # Aqui é criada uma chave estrangeira, que servirá para relacionar as duas tabelas Recipe e Category. Os parametros deste elemento são (O primeiro indica de qual outra classe vem a relação, o segundo faz com que caso essa categoria seja excluida automaticamente será atribuido o valor NULL para este elemento para que não haja inconsistência nos dados, e o terceiro parâmetro permite com que essa ação seja feita)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    # Aqui é criada uma chave estrangeira para o autor da receita, com as mesmas caracteristicas do elemento anterior, porém neste caso não precisaremos criar uma classe de usuário manualmente, pois fizemos isso apartir de um import do django que já disponibiliza uma classe User pré criada para nós
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
