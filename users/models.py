from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson


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


class Payments(models.Model):
    PAYMENTS_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Безнал'),
    ]

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, verbose_name='пользователь', blank=True, null=True)
    payment_date = models.DateField(default=timezone.now(), verbose_name='дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс',
                                    blank=True, null=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок',
                                    blank=True, null=True)
    payment_sum = models.FloatField(verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=50, verbose_name='способ оплаты', choices=PAYMENTS_CHOICES)


    def __str__(self):
        return f"{self.user} ({self.paid_course if self.paid_course else self.paid_lesson})-оплачено {self.payment_sum}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ('-payment_date',)


class Subscription(models.Model):
    """Класс подписки на курс"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'