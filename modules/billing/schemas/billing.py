from pydantic import BaseModel


class CheckoutResponse(BaseModel):
    checkout_url: str

class SubscriptionResponse(BaseModel):
    plan_id: int
    status: str

class CreateSubscriptionRequest(BaseModel):
    plan_id: int        