from mongoengine import Document, StringField, EmailField, DateTimeField,IntField
from datetime import datetime

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    credits = IntField(default=0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'users'
    }
