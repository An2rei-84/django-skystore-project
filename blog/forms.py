from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    """
    Форма для создания и редактирования объектов модели Blog.
    """
    class Meta:
        model = Blog
        fields = ['title', 'content', 'preview', 'is_published', 'slug']