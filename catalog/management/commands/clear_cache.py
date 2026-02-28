from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    """
    Кастомная команда Django для очистки кэша.
    """
    help = 'Очищает весь кэш Django.'

    def handle(self, *args, **options):
        """
        Основной метод команды.
        """
        self.stdout.write('Очистка кэша...')
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Кэш успешно очищен.'))
