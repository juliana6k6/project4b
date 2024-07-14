from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from users.models import Subscription, User
from django.utils import timezone


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
def check_user_activity(user_id):
    """Функция проверки активности пользователя"""
    delta_time = timezone.now() - timezone.timedelta(days=30)
    user = User.objects.get(id=user_id)
    if user.last_login < delta_time:
        user.is_active = False
        user.save()

    # users_list = User.objects.filter(is_active=True, is_superuser=False, last_login__isnull=False)
    #
    # for user in users_list:
    #     if user.last_login < (timezone.now() - timedelta(days=30)):
    #         user.is_active = False
    #         user.save()