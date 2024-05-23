import stripe
from config import settings
from django.shortcuts import get_object_or_404
from materials.models import Course
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from services import create_product, create_price, create_session

from users.models import User, Payments, Subscription

from users.serializers import (
    UserSerializer,
    UserDetailSerializer,
    SubscriptionSerializer, PaymentSerializer,
)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)  # сделали пользователя активным
        user.set_password(user.password)  # хешируется пароль
        user.save()


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()



class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        # получаем пользователя из self.requests
        course_id = self.request.data.get("course")
        # получаем id курса из self.request.data
        course_item = get_object_or_404(Course, pk=course_id)
        # получаем объект курса из базы с помощью get_object_or_404
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        # объекты подписок по текущему пользователю и курсу

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            # Если подписка у пользователя на этот курс есть - удаляем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
            # Если подписки у пользователя на этот курс нет - создаем ее
        return Response({"message": message})

class PaymentsListAPIView(generics.ListAPIView):
    """Просмотр списка платежей с фильтрацией по курсу, уроку и способу оплаты,
       и с сортировкой по дате(по умолчанию в модели сортировка по убыванию,
       при запросе можно изменить с помощью -"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payments = serializer.save(user=self.request.user)
        product_id = create_product(payments)
        price_id = create_price(payments, product_id)
        session_id, payments_link = create_session(price_id)
        payments.session_id = session_id
        payments.payments_link = payments_link
        payments.save()

