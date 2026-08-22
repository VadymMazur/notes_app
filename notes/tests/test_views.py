from datetime import date

import pytest
from django.urls import reverse

from ..models import Note


@pytest.mark.django_db
def test_note_create_api(authenticated_client, user, category):
    url = reverse('note_create')
    response = authenticated_client.post(
        url,
        {
            'title': 'Нова нотатка',
            'text': 'Текст нової нотатки',
            'reminder': '2026-09-01',
            'category': category.pk,
        },
    )

    assert response.status_code == 302
    note = Note.objects.get(title='Нова нотатка')
    assert note.text == 'Текст нової нотатки'
    assert note.reminder == date(2026, 9, 1)
    assert note.category == category
    assert note.user == user


@pytest.mark.django_db
def test_note_update_api(authenticated_client, note, category):
    url = reverse('note_edit', args=[note.pk])
    response = authenticated_client.post(
        url,
        {
            'title': 'Змінена нотатка',
            'text': 'Змінений текст нотатки',
            'reminder': '2026-09-10',
            'category': category.pk,
        },
    )
    note.refresh_from_db()

    assert response.status_code == 302
    assert note.title == 'Змінена нотатка'
    assert note.text == 'Змінений текст нотатки'
    assert note.reminder == date(2026, 9, 10)
    assert note.category == category
