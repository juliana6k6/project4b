from django.urls import path
# from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import PaymentListView
from users.views import UserListAPIView, UserCreateAPIView, UserDetailAPIView, UserUpdateAPIView, UserDeleteAPIView

app_name = UsersConfig.name

# router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('user/', UserListAPIView.as_view(), name='user_list'),
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user_delete'),
    path('payments/', PaymentListView.as_view(), name='payment_list'),
            ] \
              # + router.urls