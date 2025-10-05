from mongoengine import Document,ReferenceField, StringField, EmailField, DateTimeField, FloatField
from datetime import datetime
from .user_model import User


class Transation(Document):
    user = ReferenceField(User, required=True)
    amount = FloatField(required=True)
    currency = StringField(default="INR")
    credits_purchased = FloatField(required=True)
    status = StringField(choices=["pending", "completed", "failed"], default="pending")
    payment_gateway_id = StringField()  # e.g., Razorpay Payment ID
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'transactions'
    }