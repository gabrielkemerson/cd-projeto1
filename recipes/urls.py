from django.urls import path
from recipes.views import Home, Contato, Sobre


urlpatterns = [
    path("", Home),
    path("sobre/", Sobre),
    path("ctt/", Contato)
]
