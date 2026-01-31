from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Модель для представления категорий продуктов.
    """
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """
    Модель для представления продуктов.
    """
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', null=True, blank=True, default='products/placeholder.svg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]


class Contact(models.Model):
    """
    Модель для хранения контактной информации компании.
    """
    country = models.CharField(max_length=100, verbose_name='Страна')
    inn = models.CharField(max_length=20, verbose_name='ИНН')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return f'{self.country} - {self.address}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Feedback(models.Model):
    """
    Модель для хранения сообщений обратной связи от пользователей.
    """
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    def __str__(self):
        return f'{self.name} ({self.phone})'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'