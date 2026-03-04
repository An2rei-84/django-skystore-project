"""
URL-маршруты для приложения "Блог".
Определяет адреса для CRUD-операций со статьями блога.
"""
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),  # Список всех опубликованных статей
    path('create/', BlogCreateView.as_view(), name='create'),  # Создание новой статьи
    path('view/<str:slug>/', BlogDetailView.as_view(), name='detail'),  # Детальный просмотр статьи по slug
    path('edit/<str:slug>/', BlogUpdateView.as_view(), name='update'),  # Редактирование статьи по slug
    path('delete/<str:slug>/', BlogDeleteView.as_view(), name='delete'),  # Удаление статьи по slug
]
