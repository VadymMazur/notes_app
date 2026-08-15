from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import NoteForm
from .models import Category, Note


class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.select_related('category').all()
        category = self.request.GET.get('category')
        reminder = self.request.GET.get('reminder')
        search = self.request.GET.get('search', '').strip()
        if category:
            queryset = queryset.filter(category_id=category)
        if reminder:
            queryset = queryset.filter(reminder=reminder)
        if search:
            value = search.casefold()
            ids = [pk for pk, title in queryset.values_list('pk', 'title') if value in title.casefold()]
            queryset = queryset.filter(pk__in=ids)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    context_object_name = 'note'

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    context_object_name = 'note'
    success_url = reverse_lazy('note_list')
