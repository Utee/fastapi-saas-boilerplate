import stripe
from fastapi import APIRouter, Request, HTTPException, Header, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.core.database import get_session
from app.services.stripe import create_checkout_session

router = APIRouter()

@router.post("/create-checkout")
async def checkout(price_id: str, user_email: str):
    try:
        url = await create_checkout_session(
            customer_email=user_email,
            price_id=price_id,
            success_url="https://yourdomain.com/dashboard?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/pricing"
        )
        return {"checkout_url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook payload or signature")

    # Handle subscription status updates
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Logic to update user subscription status in DB
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # Logic to revoke paid access in DB

    return {"status": "success"}