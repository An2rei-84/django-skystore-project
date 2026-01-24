from django import forms
from .models import Product, Feedback

class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования объектов модели Product.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

class FeedbackForm(forms.ModelForm):
    """
    Форма для отправки сообщений обратной связи.
    """
    class Meta:
        model = Feedback
        fields = ['name', 'phone', 'message']
