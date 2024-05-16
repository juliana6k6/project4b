from django.shortcuts import get_object_or_404
from materials.models import Course
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Payments, Subscription

from users.serializers import UserSerializer, UserDetailSerializer, SubscriptionSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True) #сделали пользователя активным
        user.set_password(user.password) #хешируется пароль
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


# class PaymentListView(generics.ListAPIView):
#     """Просмотр списка платежей с фильтрацией по курсу, уроку и способу оплаты,
#        и с сортировкой по дате(по умолчанию в модели сортировка по убыванию,
#        при запросе можно изменить с помощью -"""
#     serializer_class = PaymentSerializer
#     queryset = Payments.objects.all()
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
#     ordering_fields = ('payment_date',)

class SubscriptionView(APIView):
    """Контроллер управления подпиской пользователя на курс
       в запросе передаем id курса и если подписка на данный курс у текущего пользователя
       существует - удаляем, если нет - создаем"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # получаем пользователя из self.requests
        course_id = self.request.data.get('course_id')
        # получаем id курса из self.reqests.data
        queryset = Course.objects.filter(pk=course_id)
        #получаем список курсов
        course = get_object_or_404(queryset=queryset)
        #получаем объект курса из базы с помощью get_object_or_404
        subs_item = Subscription.objects.filter(course=course, user=user)
        # объекты подписок по текущему пользователю и курсу

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        # Если подписка у пользователя на этот курс есть - удаляем ее

        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        return Response({"message": message})
        # Возвращаем ответ в API
