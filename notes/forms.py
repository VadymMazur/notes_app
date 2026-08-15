from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'reminder', 'category']
        labels = {'title': 'Назва', 'text': 'Текст', 'reminder': 'Дата нагадування', 'category': 'Категорія'}
        widgets = {
            'reminder': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'rows': 6}),
        }
