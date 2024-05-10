from rest_framework import serializers
from users.models import Payments, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профиля пользователя, включает поле истории платежей"""
    payment_list = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = '__all__'