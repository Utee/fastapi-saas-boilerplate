import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY

async def create_checkout_session(customer_email: str, price_id: str, success_url: str, cancel_url: str) -> str:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer_email=customer_email,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url

async def create_customer_portal_session(customer_id: str, return_url: str) -> str:
    portal = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return portal.url