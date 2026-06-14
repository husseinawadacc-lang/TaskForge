import stripe
from fastapi import Depends, Request, HTTPException, APIRouter

from core.config import get_settings
from api.deps.services_dep import get_unit_of_work
from modules.billing.depends.dependencies import get_billing_service
import traceback
settings = get_settings()

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    billing=Depends(get_billing_service),
    uow=Depends(get_unit_of_work)
):
    print("Received webhook request")
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    print("signature header:", sig_header  )
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
        print("WEBHOOK HIT")
        print("event type:", event["type"])
    except stripe.error.SignatureVerificationError as e:
         print("Signature Error:", str(e))
         traceback.print_exc()
       
         raise HTTPException(status_code=400, detail="Invalid signature")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 🎯 event handling
    if event["type"] == "checkout.session.completed":

        session_data = event["data"]["object"]

        user_id = int(session_data["metadata"]["user_id"])
        plan_id = int(session_data["metadata"]["plan_id"])

        with uow as session:
            billing.upgrade_plan(
                session=session,
                user_id=user_id,
                new_plan_id=plan_id
            )

    return {"status": "success"}