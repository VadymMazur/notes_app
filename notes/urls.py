from django.urls import path
from .views import hello_from_Notes_app

urlpatterns = [
    path("hello/", hello_from_Notes_app),
]