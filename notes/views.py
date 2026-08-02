import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse


def hello_from_notes_app(request):
    context = {
        'title': 'Моя сторінка',
        'message': 'Привіт світ!',
        'products': ['element1', 'element2', 'element3']
    }
    return render(request, 'index.html', context)