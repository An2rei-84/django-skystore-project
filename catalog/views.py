from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)

from .models import Product, Contact, Feedback
from .forms import ProductForm, FeedbackForm


class ProductListView(ListView):
    """
    Представление для отображения списка продуктов с пагинацией.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        """
        Возвращает queryset продуктов, отсортированных по дате создания (сначала новые).
        """
        return Product.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст пагинацию и заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        
        # Ручная пагинация
        paginator = Paginator(self.get_queryset(), 5) # 5 продуктов на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context[self.context_object_name] = page_obj
        context['title'] = 'Skystore'
        return context


class ContactFormView(FormView):
    """
    Представление для страницы контактов и обработки формы обратной связи.
    """
    template_name = 'catalog/contacts.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('catalog:contacts')

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст статическую контактную информацию.
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра продукта.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Skystore - {self.object.name}'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить продукт'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования продукта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления продукта.
        """
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать {self.object.name}'
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления продукта.
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удалить {self.object.name}'
        return context