from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
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
        Возвращает queryset опубликованных продуктов, отсортированных по дате создания.
        """
        return Product.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст пагинацию и заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        
        paginator = Paginator(self.get_queryset(), 5)
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
    Автоматически назначает текущего пользователя владельцем продукта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """
        Присваивает текущего пользователя как владельца продукта перед сохранением.
        """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить продукт'
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для редактирования продукта.
    Доступно только для владельца продукта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        """
        Проверяет, является ли текущий пользователь владельцем продукта.
        """
        return self.request.user == self.get_object().owner

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


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Представление для удаления продукта.
    Доступно для владельца или модератора.
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        """
        Проверяет, является ли пользователь владельцем продукта или имеет право на удаление.
        """
        product = self.get_object()
        is_owner = self.request.user == product.owner
        can_delete = self.request.user.has_perm('catalog.delete_product')
        return is_owner or can_delete

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удалить {self.object.name}'
        return context


@login_required
@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    """
    Контроллер для отмены публикации продукта.
    Доступен только для пользователей с правом 'can_unpublish_product'.
    """
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:product_detail', pk=pk)