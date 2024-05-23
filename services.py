import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создаем stripe продукт"""
    stripe_product = stripe.Product.create(name=product.title)
    return stripe_product.get("id")


def create_price(money, id_product):
    """Создаём stripe цену"""
    stripe_price = stripe.Price.create(currency='RUB', unit_amount=int(money * 100), product=id_product)
    return stripe_price.get("id")


def create_session(price):
    """Создаём stripe сессию"""
    stripe_session = stripe.checkout.Session.create(success_url="http://127.0.0.1:8000",
                                                    line_items=[{"price": price.get('id'), "quantity": 1}],
                                                    mode="payment")
    return stripe_session.get("id"), stripe_session.get("url")