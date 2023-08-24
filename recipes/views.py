from django.shortcuts import render
from utils.recipes.factory import make_recipe
from . models import Recipe
from django.http import HttpResponse

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    # recipes recebe todos os objetos de Recipe filtrados por(id e que estejam publicados) os objetos serão ordenados por ordem decrescente dos ID
    recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    
    if not recipes:
        return HttpResponse(content='Not foun page', status='404')

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes.first().category.name}  - Category'
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'contador': make_recipe(),
        'is_detail_page': True,
    })
