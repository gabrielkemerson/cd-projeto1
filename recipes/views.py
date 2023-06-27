from django.shortcuts import render
from django.http import HttpResponse


def Home(request):
    return render(request, 'recipes/home.html', context={
        'name': 'Usuário',
    })


def Contato(request):
    return render(request, 'recipes/ctt.html')


def Sobre(request):
    return render(request, 'recipes/sobre.html')
