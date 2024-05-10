from django.urls import path
# from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import PaymentListView
from users.views import UserListAPIView, UserCreateAPIView, UserDetailAPIView, UserUpdateAPIView, UserDeleteAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


app_name = UsersConfig.name

# router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserListAPIView.as_view(), name='user_list'),
    path('user/create/', UserCreateAPIView.as_view(), name='user_register'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user_delete'),
    path('payments/', PaymentListView.as_view(), name='payment_list'),
            ] \
              # + router.urls