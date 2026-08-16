from django.contrib import admin

from .models import Category, Note, NoteGroup


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'reminder', 'user')
    list_filter = ('category', 'reminder')
    search_fields = ('title', 'text', 'user__username')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class NoteGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('members', 'notes')


admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NoteGroup, NoteGroupAdmin)
