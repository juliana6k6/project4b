from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=35, verbose_name="номер телефона", blank=True, null=True,
                                    help_text='Укажите номер телефона')
    avatar = models.ImageField(upload_to='users/avatar/', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите аватар')
    city = models.CharField(max_length=50, verbose_name="город", blank=True, null=True, help_text='Укажите город')
    email = models.EmailField(unique=True, verbose_name="Email", help_text='Укажите город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
