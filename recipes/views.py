from django.shortcuts import render


def Home(request):
    return render(request, 'recipes/pages/home.html')


def Recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html')
