from django.shortcuts import render

from .models import Note


def hello_from_notes_app(request):
    notes = Note.objects.select_related('category').all()

    context = {
        'title': 'Мої нотатки',
        'notes': notes,
    }
    return render(request, 'index.html', context)
