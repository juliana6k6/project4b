import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_product():
    """Создаем stripe продукт"""
    stripe_product = stripe.Product.create(name='Payment_course')
    return stripe_product.get("id")


def create_stripe_price(amount):
    """Создаём stripe цену"""
    return stripe.Price.create(
        currency='rub',
        unit_amount=int(amount * 100),
        product_data={'name': 'Payments'},)


def create_stripe_session(price):
    """Создаём stripe сессию"""
    session = stripe.checkout.Session.create(success_url="http://127.0.0.1:8000/users/payments_list",
                                             line_items=[{"price": price.get("id"), "quantity": 1}],
                                             mode="payment")
    return session.get("id"), session.get("url")
