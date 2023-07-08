from django.shortcuts import render


def Home(request):
    return render(request, 'recipes/pages/home.html')
