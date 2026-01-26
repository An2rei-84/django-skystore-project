from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', null=True, blank=True)
    phone_number = models.CharField(max_length=35, verbose_name='Номер телефона', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='Страна', null=True, blank=True)

    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'