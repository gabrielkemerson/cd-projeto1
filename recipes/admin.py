from django.contrib import admin

# Este é o import dos models criados em recipes
from . models import Category, Recipe


# Aqui é criado uma classe que irá corresponder a um determinado model
class CategoryAdmin(admin.ModelAdmin):
    ...

# Aqui também
class RecipeAdmin(admin.ModelAdmin):
    ...

# Na linha de código a baixo pe feira a relação entre uma classe e um model e este model é posteriormente adicionado a pagina de admin do Django.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
