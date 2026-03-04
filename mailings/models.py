from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """
    Модель для представления рассылки.
    """
    # Статусы рассылки
    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_COMPLETED = 'completed'
    STATUS_PAUSED = 'paused'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
        (STATUS_PAUSED, 'Приостановлена'),
    ]

    # Периодичность рассылки
    FREQUENCY_DAILY = 'daily'
    FREQUENCY_WEEKLY = 'weekly'
    FREQUENCY_MONTHLY = 'monthly'
    FREQUENCY_CHOICES = [
        (FREQUENCY_DAILY, 'Раз в день'),
        (FREQUENCY_WEEKLY, 'Раз в неделю'),
        (FREQUENCY_MONTHLY, 'Раз в месяц'),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='Статус')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    clients = models.ManyToManyField('Client', verbose_name='Клиенты рассылки')

    def __str__(self):
        return (f'Рассылка с {self.start_time.strftime("%H:%M %d-%m-%Y")} '
                f'по {self.end_time.strftime("%H:%M %d-%m-%Y")} ({self.get_frequency_display()})')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("can_set_mailing_status", "Can set mailing status"),
            ("view_any_mailing", "Can view any mailing"),
            ("change_any_mailing", "Can change any mailing"),
            ("delete_any_mailing", "Can delete any mailing"),
        ]


class Message(models.Model):
    """
    Модель для представления сообщения, отправляемого в рассылке.
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ("view_any_message", "Can view any message"),
            ("change_any_message", "Can change any message"),
            ("delete_any_message", "Can delete any message"),
        ]


class Client(models.Model):
    """
    Модель для представления клиента рассылки.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        permissions = [
            ("view_any_client", "Can view any client"),
            ("change_any_client", "Can change any client"),
            ("delete_any_client", "Can delete any client"),
        ]


class Attempt(models.Model):
    """
    Модель для представления попытки отправки рассылки.
    """
    # Статусы попытки
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Неуспешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'Попытка для {self.mailing} от {self.timestamp.strftime("%H:%M %d-%m-%Y")} - {self.get_status_display()}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
