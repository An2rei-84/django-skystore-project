import smtplib
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from mailings.models import Mailing, Attempt, Message


class Command(BaseCommand):
    """
    Кастомная команда Django для отправки запланированных рассылок.
    """
    help = 'Итерирует все активные рассылки и отправляет email, если пришло время.'

    def handle(self, *args, **options):
        """
        Основной метод команды.
        """
        now = timezone.now()
        # Выбираем активные рассылки, которые еще не завершились
        active_mailings = Mailing.objects.filter(
            status=Mailing.STATUS_STARTED
        ).filter(
            start_time__lte=now,
            end_time__gte=now
        )

        self.stdout.write(f"Найдено {active_mailings.count()} активных рассылок для проверки.")

        for mailing in active_mailings:
            last_attempt = Attempt.objects.filter(mailing=mailing).order_by('-timestamp').first()

            # Определяем, пора ли отправлять рассылку
            send_needed = False
            if not last_attempt:
                send_needed = True
            else:
                if mailing.frequency == Mailing.FREQUENCY_DAILY:
                    if now - last_attempt.timestamp >= timedelta(days=1):
                        send_needed = True
                elif mailing.frequency == Mailing.FREQUENCY_WEEKLY:
                    if now - last_attempt.timestamp >= timedelta(weeks=1):
                        send_needed = True
                elif mailing.frequency == Mailing.FREQUENCY_MONTHLY:
                    # Приблизительный расчет для месяца
                    if now - last_attempt.timestamp >= timedelta(days=30):
                        send_needed = True

            if send_needed:
                self.stdout.write(self.style.SUCCESS(f"Отправка рассылки: {mailing}"))
                try:
                    # Получаем сообщение и клиентов для рассылки
                    message = Message.objects.get(mailing=mailing)
                    clients = mailing.clients.all()

                    if not clients:
                        self.stdout.write(self.style.WARNING(f"Нет клиентов для рассылки {mailing}."))
                        continue

                    # Отправляем email каждому клиенту
                    recipient_emails = [client.email for client in clients]
                    sent_count = send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=None,  # Использует DEFAULT_FROM_EMAIL
                        recipient_list=recipient_emails,
                        fail_silently=False,
                    )

                    # Логируем успешную попытку
                    if sent_count > 0:
                        Attempt.objects.create(
                            mailing=mailing,
                            status=Attempt.STATUS_SUCCESS,
                            server_response=f"Успешно отправлено {sent_count} из {len(recipient_emails)} писем."
                        )
                        self.stdout.write(self.style.SUCCESS(f"Успешно отправлено для рассылки {mailing}."))
                    else:
                        raise smtplib.SMTPException("send_mail вернул 0.")

                except Exception as e:
                    # Логируем неудавшуюся попытку
                    Attempt.objects.create(
                        mailing=mailing,
                        status=Attempt.STATUS_FAILED,
                        server_response=str(e)
                    )
                    self.stdout.write(self.style.ERROR(f"Ошибка при отправке рассылки {mailing}: {e}"))

        # Завершаем рассылки, у которых вышло время
        completed_mailings = Mailing.objects.filter(
            status=Mailing.STATUS_STARTED,
            end_time__lt=now
        )
        for mailing in completed_mailings:
            mailing.status = Mailing.STATUS_COMPLETED
            mailing.save()
            self.stdout.write(f"Рассылка {mailing} завершена по времени.")
