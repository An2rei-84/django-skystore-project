from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy

from .models import Product, Contact, Feedback
from .forms import ProductForm, FeedbackForm


class ProductListView(ListView):
    """
    Представление для отображения списка продуктов с пагинацией.
    Использует ListView для автоматической обработки списка объектов.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 3  # Показывать 3 товара на странице

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок страницы в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore'
        return context

class ContactFormView(FormView):
    """
    Представление для отображения страницы контактов и обработки формы обратной связи.
    Использует FormView для обработки POST-запросов и сохранения данных обратной связи.
    """
    template_name = 'catalog/contacts.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('catalog:contacts') # URL для перенаправления после успешной отправки формы

    def get_context_data(self, **kwargs):
        """
        Добавляет контактную информацию в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['contact_info'] = {
            'country': 'Россия',
            'inn': '1234567890',
            'address': 'г. Москва, ул. Примерная, д. 1'
        }
        return context

    def form_valid(self, form):
        """
        Сохраняет данные формы обратной связи.
        """
        form.save()
        return super().form_valid(form)

class ProductDetailView(DetailView):
    """
    Представление для отображения детальной информации об одном продукте.
    Использует DetailView для автоматического извлечения объекта по его первичному ключу.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок страницы в контекст, используя имя продукта.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Skystore - {self.object.name}'
        return context

class ProductCreateView(CreateView):
    """
    Представление для создания нового продукта.
    Использует CreateView для обработки формы создания объекта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home') # URL для перенаправления после успешного создания продукта

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок страницы в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить продукт'
        return context