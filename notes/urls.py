from django.urls import path

from .views import NoteCreateView, NoteDeleteView, NoteDetailView, NoteListView, NoteUpdateView

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]
