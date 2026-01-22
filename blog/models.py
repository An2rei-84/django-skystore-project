from django.db import models

class Blog(models.Model):
    """
    Модель для представления записи в блоге.
    Содержит информацию о статье, такую как заголовок, содержимое, изображение,
    дату создания, статус публикации и счетчик просмотров.
    """
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    # Slug для формирования ЧПУ (человекопонятного URL). Генерируется автоматически из заголовка.
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'