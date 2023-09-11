from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe    # noqa
from . models import Recipe
from django.http import HttpResponse    # noqa


def home(request):

    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    # recipes recebe todos os objetos de Recipe filtrados por(que tenham o mesmo id de category, e que estejam publicados) os objetos serão ordenados por ordem decrescente dos ID    # noqa
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))    # noqa

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}  - Category'
    })


def recipe(request, id):
    # Lembre-se que os filtros não são pk recebe id, mas se pk for igual ao id, ou seja etá mais pra um if do que um recebe    # noqa
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'contador': recipe,
        'is_detail_page': True,
    })
