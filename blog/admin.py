from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Административный класс для модели Blog.
    Определяет отображение полей и функционал в админ-панели Django.
    """
    list_display = ('title', 'slug', 'is_published', 'views_count', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    # Автоматически заполняет поле 'slug' на основе 'title' при создании/редактировании
    prepopulated_fields = {'slug': ('title',)}