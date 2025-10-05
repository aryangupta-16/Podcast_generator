from fastapi import APIRouter, HTTPException,FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from utils.dependencies import get_current_user
from fastapi import Depends
from models.user_model import User

load_dotenv()

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")

PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com" 

router = APIRouter(prefix="/api/v1", tags=["order"])

class OrderRequest(BaseModel):
    amount: str
    currency: str = "USD"


def _get_basic_auth_from_env() -> str:
    """
    Returns Base64(client_id:client_secret).
    Prefers PAYPAL_BASIC_AUTH if present; otherwise builds from client id/secret.
    """
    b64 = os.getenv("PAYPAL_BASIC_AUTH")
    if b64:
        return b64

    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing PayPal credentials: set PAYPAL_BASIC_AUTH or PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET"
        )
    raw = f"{client_id}:{client_secret}".encode("ascii")
    return base64.b64encode(raw).decode("ascii")


def get_access_token():
    """Fetch PayPal OAuth2 token"""

    data = {"grant_type": "client_credentials"}

    basic_auth = _get_basic_auth_from_env()

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    resp = requests.post(f"{PAYPAL_API_BASE}/v1/oauth2/token", headers=headers, data=data, timeout=10)
    resp.raise_for_status()
    body = resp.json()

    token = body.get("access_token")
    expires_in = int(body.get("expires_in", 32400))

    if not token:
        raise RuntimeError("No access_token in PayPal response: " + resp.text)

    return token

@router.post("/orders")
def create_order(order: OrderRequest,current_user = Depends(get_current_user)):
    """Create PayPal order with amount from frontend"""
    access_token = get_access_token()
    print(access_token,"access_token")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}

    print(order.amount)
    body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": order.amount
                }
            }
        ]
    }

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders",
        headers=headers, json=body
    )
    response.raise_for_status()
    return response.json()

@router.post("/orders/{order_id}/capture")
def capture_order(order_id: str,current_user = Depends(get_current_user)):
    """Capture a PayPal order"""
    access_token = get_access_token()

    user_id = current_user.id
    email = current_user.email

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture",
        headers=headers
    )

    user = User.objects(email=current_user.email).first()
    amount_value = response.json()["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"]
    user.credits += int(float(amount_value))
    user.save();
    response.raise_for_status()
    return response.json()
