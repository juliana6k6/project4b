from celery import shared_task
from config.settings import EMAIL_HOST_USER, TIME_ZONE
from django.core.mail import send_mail
from users.models import Subscription, User
# from django.utils import timezone
# from datetime import timedelta
import pytz
import datetime


@shared_task
def mail_update_course_info(course_id):
    """Функция отправки сообщения об обновлении курса"""
    course_subscriptions = Subscription.objects.filter(course=course_id)
    for subscription in course_subscriptions:
        send_mail(
            subject="Обновление материалов курса",
            message=f'Курс {subscription.course.title} был обновлен.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False
        )


@shared_task
def check_user_activity():
    """Функция проверки активности пользователя"""
    users = User.objects.filter(is_active=True, is_superuser=False,  last_login__isnull=False)
    if users.exists():
        for user in users:
            print("start!")
            # if user.last_login < (timezone.now() - timedelta(minutes=2)):
            #     user.is_active = False
            #     user.save()
            if datetime.datetime.now(pytz.timezone("Europe/Moscow")) - user.last_login > datetime.timedelta(weeks=4):
                user.is_active = False
                user.save()


