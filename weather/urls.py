from django.urls import path
from weather import views

urlpatterns = [
    path("weather/<name>", views.weather, name="data"),
    path("", views.home, name="home"),
]