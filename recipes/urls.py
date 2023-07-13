from django.urls import path
from . import views


urlpatterns = [
    path("", views.Home),
    path("recipes/<int:id>/", views.Recipe),
]
