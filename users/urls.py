from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
            path('payments/', PaymentListView.as_view(), name='payment_list'),
            ] + router.urls