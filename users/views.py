from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User, Payments


from users.serializers import UserSerializer, UserDetailSerializer


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
