from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Category, Note


class NoteViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Робота')
        self.note = Note.objects.create(title='Зустріч із командою', text='Текст', reminder=date(2026, 8, 20), category=self.category)

    def test_list_detail_create_update_delete(self):
        self.assertContains(self.client.get(reverse('note_list')), self.note.title)
        self.assertContains(self.client.get(reverse('note_detail', args=[self.note.pk])), self.note.text)
        response = self.client.post(reverse('note_create'), {'title': 'Нова', 'text': 'Текст', 'reminder': '2026-08-21', 'category': self.category.pk})
        self.assertRedirects(response, reverse('note_list'))
        response = self.client.post(reverse('note_edit', args=[self.note.pk]), {'title': 'Оновлена', 'text': 'Текст', 'reminder': '2026-08-20', 'category': self.category.pk})
        self.assertRedirects(response, reverse('note_detail', args=[self.note.pk]))
        response = self.client.post(reverse('note_delete', args=[self.note.pk]))
        self.assertRedirects(response, reverse('note_list'))

    def test_search_and_filters(self):
        response = self.client.get(reverse('note_list'), {'search': 'зустріч ІЗ КОМАНДОЮ', 'category': self.category.pk, 'reminder': '2026-08-20'})
        self.assertContains(response, self.note.title)

    def test_bootstrap_navigation_and_form(self):
        list_response = self.client.get(reverse('note_list'))
        form_response = self.client.get(reverse('note_create'))
        self.assertContains(list_response, 'bootstrap@5.3.8')
        self.assertContains(list_response, reverse('note_list'))
        self.assertContains(list_response, reverse('note_create'))
        self.assertContains(form_response, 'class="form-control"')
        self.assertContains(form_response, 'class="form-select"')
        self.assertContains(list_response, 'bootstrap.bundle.min.js')
        self.assertContains(list_response, 'class="navbar-toggler"')
