from mongoengine import Document, StringField, DateTimeField, ReferenceField, FloatField
from datetime import datetime
from .user_model import User

class Podcast(Document):
    title = StringField(required=True)
    topic = StringField(required=True)
    audio_url = StringField(required=True)  # Link to generated audio file (S3, GCP, etc.)
    transcript = StringField()  # Generated transcript text
    duration_seconds = FloatField()
    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'podcasts'
    }
