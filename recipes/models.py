from django.db import models

# Create your models here.

class Recipe(models.Model):
    # Cria uma coluna chamada 'title' que recebe um CharField(que é o equivalente ao VarChar no SQL) que pode receber no máximo 65 caracteres
    title = models.CharField(max_length=65)
    # Cria uma coluna chamada description que também recebe um Charfield de no máximo 200 caracteres
    description = models.CharField(max_length=200)
    # Basicamente é usado como identificador único como se fosse uma Primary Key
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
    cover = models.ImageField(upload_to='recipes/covers/%y/%m/%d')
