from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_pk: int):
    """
    Возвращает queryset всех опубликованных продуктов в указанной категории.
    Реализует низкоуровневое кеширование.
    """
    category = Category.objects.get(pk=category_pk)

    if settings.CACHE_ENABLED:
        # Формируем ключ для кеша
        key = f'category_products_{category_pk}'
        # Пытаемся получить данные из кеша
        products = cache.get(key)
        if products is None:
            # Если данных в кеше нет, получаем их из БД
            products = Product.objects.filter(category=category, is_published=True)
            # Сохраняем данные в кеш
            cache.set(key, products)
    else:
        # Если кеширование отключено, просто получаем данные из БД
        products = Product.objects.filter(category=category, is_published=True)

    return category, products
