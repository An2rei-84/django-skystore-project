
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import Blog
from mailings.models import Mailing, Message, Client  # Import mailings models


class Command(BaseCommand):
    """
    Кастомная команда для создания групп пользователей и назначения им прав.
    """

    help = 'Создает группы "Модератор продуктов" и "Контент-менеджер" и назначает им права.'

    def handle(self, *args, **options):
        """
        Основной метод команды, который выполняет создание групп и назначение прав.
        """
        # --- Группа Модераторов ---
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераator продуктов" успешно создана.'))

        product_content_type = ContentType.objects.get_for_model(Product)
        try:
            can_unpublish_permission = Permission.objects.get(
                codename='can_unpublish_product', content_type=product_content_type
            )
            delete_product_permission = Permission.objects.get(
                codename='delete_product', content_type=product_content_type
            )
            moderator_group.permissions.add(
                can_unpublish_permission, delete_product_permission
            )
            self.stdout.write(
                self.style.SUCCESS('Права для "Модератора продуктов" успешно назначены.')
            )
        except Permission.DoesNotExist:
            self.stderr.write(self.style.ERROR('Не найдены права для модели Product.'))

        # --- Группа Контент-менеджеров ---
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Контент-менеджер" успешно создана.')
            )

        blog_content_type = ContentType.objects.get_for_model(Blog)
        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        message_content_type = ContentType.objects.get_for_model(Message)
        client_content_type = ContentType.objects.get_for_model(Client)

        try:
            # Blog permissions
            add_blog_permission = Permission.objects.get(codename='add_blog', content_type=blog_content_type)
            change_blog_permission = Permission.objects.get(codename='change_blog', content_type=blog_content_type)
            delete_blog_permission = Permission.objects.get(codename='delete_blog', content_type=blog_content_type)

            # Mailing permissions
            can_set_mailing_status = Permission.objects.get(codename='can_set_mailing_status', content_type=mailing_content_type)
            view_any_mailing = Permission.objects.get(codename='view_any_mailing', content_type=mailing_content_type)

            # Message permissions
            view_any_message = Permission.objects.get(codename='view_any_message', content_type=message_content_type)

            # Client permissions
            view_any_client = Permission.objects.get(codename='view_any_client', content_type=client_content_type)

            content_manager_group.permissions.add(
                add_blog_permission, change_blog_permission, delete_blog_permission,
                can_set_mailing_status, view_any_mailing,
                view_any_message,
                view_any_client
            )
            self.stdout.write(
                self.style.SUCCESS('Права для "Контент-менеджера" успешно назначены.')
            )
        except Permission.DoesNotExist:
            self.stderr.write(self.style.ERROR('Не найдены права для моделей Blog или Mailings.'))
