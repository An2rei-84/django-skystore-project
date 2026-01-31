from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from slugify import slugify as slugify_lib # Используем slugify из python-slugify

from .models import Blog
from .forms import BlogForm

class BlogListView(ListView):
    """
    Представление для отображения списка статей блога.
    Использует ListView для автоматической обработки списка объектов.
    """
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_posts'

    def get_queryset(self, *args, **kwargs):
        """
        Переопределяет queryset для отображения только опубликованных статей.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)  # Фильтрация по опубликованным статьям
        return queryset

class BlogDetailView(DetailView):
    """
    Представление для отображения детальной информации об одной статье блога.
    Использует DetailView для автоматического извлечения объекта по его slug.
    """
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        """
        Переопределяет получение объекта для увеличения счетчика просмотров
        и отправки уведомления по email при достижении 100 просмотров.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        # Дополнительное задание: отправка email при достижении 100 просмотров
        if self.object.views_count == 100:
            subject = f"Поздравляем! Статья '{self.object.title}' достигла 100 просмотров!"
            message = f"Ваша статья '{self.object.title}' только что достигла 100 просмотров на сайте."
            from_email = 'your_email@example.com'  # Замените на свой email
            recipient_list = ['your_email@example.com']  # Замените на свой email
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print(f"Email отправлен: '{self.object.title}' достигла 100 просмотров.")
            except Exception as e:
                print(f"Ошибка при отправке email: {e}")
            # Для корректной работы отправки email необходимо настроить параметры EMAIL_BACKEND, EMAIL_HOST,
            # EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD в файле settings.py.
            # Пример настройки для Gmail:
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_PORT = 587
            # EMAIL_USE_TLS = True
            # EMAIL_HOST_USER = 'your_email@gmail.com'
            # EMAIL_HOST_PASSWORD = 'your_app_password' # Используйте пароль приложения, не пароль от аккаунта Google
        return self.object

class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление для создания новой статьи блога.
    Автоматически генерирует slug из заголовка или транслитерирует введенный пользователем slug.
    Доступно только для пользователей с правом на добавление статей.
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        """
        Переопределяет сохранение формы для генерации или транслитерации slug.
        """
        # Если slug не задан или пуст, генерируем его из заголовка
        if form.instance.slug is None or not form.instance.slug:
            form.instance.slug = slugify_lib(form.instance.title)
        else:
            # Если пользователь предоставил slug, транслитерируем его для обеспечения ASCII-совместимости
            form.instance.slug = slugify_lib(form.instance.slug)
        print(f"DEBUG: Slug before saving: '{form.instance.slug}' (type: {type(form.instance.slug)})") # Отладочный вывод
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Представление для редактирования существующей статьи блога.
    Автоматически транслитерирует введенный пользователем slug, если он изменен.
    Доступно только для пользователей с правом на изменение статей.
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        """
        Переопределяет сохранение формы для генерации или транслитерации slug.
        """
        # Если slug не задан или пуст, генерируем его из заголовка
        if form.instance.slug is None or not form.instance.slug:
            form.instance.slug = slugify_lib(form.instance.title)
        else:
            # Если пользователь предоставил slug, транслитерируем его для обеспечения ASCII-совместимости
            form.instance.slug = slugify_lib(form.instance.slug)
        print(f"DEBUG: Slug before saving: '{form.instance.slug}' (type: {type(form.instance.slug)})") # Отладочный вывод
        return super().form_valid(form)

    def get_success_url(self):
        """
        Определяет URL для перенаправления после успешного обновления статьи.
        Перенаправляет на страницу детального просмотра отредактированной статьи.
        """
        return reverse_lazy('blog:detail', kwargs={'slug': self.object.slug})

class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления статьи блога.
    Доступно только для пользователей с правом на удаление статей.
    """
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'