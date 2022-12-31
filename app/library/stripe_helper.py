import os
import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_product(name: str) -> str:
    res = stripe.Product.create(name=name)
    return res["id"]


def delete_stripe_product(name: str) -> None:
    stripe.Product.delete(name=name)
