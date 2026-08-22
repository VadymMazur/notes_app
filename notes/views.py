from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import LoginForm, NoteForm, RegisterForm
from .models import Category, Note


def login_view(request):
    if request.user.is_authenticated:
        return redirect('note_list')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Вітаємо, {username}!')
                return redirect(request.GET.get('next') or 'note_list')
            messages.error(request, 'Неправильне ім’я користувача або пароль!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('note_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успішна реєстрація!')
            return redirect('note_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect('login')


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.select_related('category', 'user')
        view_type = self.request.GET.get('view_type', 'personal')
        if view_type == 'group':
            queryset = queryset.filter(groups__members=self.request.user).distinct()
        else:
            queryset = queryset.filter(user=self.request.user)
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
        context['view_type'] = self.request.GET.get('view_type', 'personal')
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.select_related('category', 'user').filter(
            Q(user=self.request.user) | Q(groups__members=self.request.user)
        ).distinct()


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    context_object_name = 'note'

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        if 'reminder' in form.changed_data:
            form.instance.reminder_sent = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    context_object_name = 'note'
    success_url = reverse_lazy('note_list')

    def test_func(self):
        return self.get_object().user == self.request.user
