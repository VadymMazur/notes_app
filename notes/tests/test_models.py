from datetime import date

import pytest

from ..models import Note


@pytest.mark.django_db
def test_note_creation(user, category):
    note = Note.objects.create(
        title='Нова нотатка',
        text='Текст нової нотатки',
        reminder=date(2026, 9, 1),
        category=category,
        user=user,
    )

    saved_note = Note.objects.get(pk=note.pk)
    assert saved_note.id is not None
    assert saved_note.title == 'Нова нотатка'
    assert saved_note.text == 'Текст нової нотатки'
    assert saved_note.reminder == date(2026, 9, 1)
    assert saved_note.category == category
    assert saved_note.user == user


@pytest.mark.django_db
def test_note_update(note):
    note.title = 'Змінена нотатка'
    note.text = 'Змінений текст нотатки'
    note.reminder = date(2026, 9, 10)
    note.save()
    note.refresh_from_db()

    assert note.title == 'Змінена нотатка'
    assert note.text == 'Змінений текст нотатки'
    assert note.reminder == date(2026, 9, 10)
