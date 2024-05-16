from django.urls import path
from rest_framework.permissions import AllowAny
# from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
# from users.views import PaymentListView
from users.views import UserCreateAPIView, UserDetailAPIView, UserUpdateAPIView, UserDeleteAPIView, UserListAPIView, \
    SubscriptionView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


app_name = UsersConfig.name

# router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserListAPIView.as_view(), name='user_list'),
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user_delete'),
    # path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('subscript/<int:pk>/', SubscriptionView.as_view(), name='sub_script'),
            ] \
              # + router.urls