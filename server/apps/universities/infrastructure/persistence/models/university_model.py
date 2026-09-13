from mongoengine import (
    Document,
    StringField,
    EmailField,
    BooleanField,
    DateTimeField,
)

from django.utils import timezone


class UniversityModel(Document):

    university_id = StringField(
        required=True,
        primary_key=True,
        max_length=50,
    )

    name = StringField(
        required=True,
        max_length=200,
    )

    domain = StringField(
        required=True,
        unique=True,
        max_length=100,
    )

    email = EmailField(
        required=True,
        unique=True,
        max_length=150,
    )

    phone = StringField(
        required=True,
        max_length=20,
    )

    is_active = BooleanField(
        default=True,
    )

    updated_at = DateTimeField(
        required=True,
        default=timezone.now,
    )

    meta = {
        "collection": "universities",
        "indexes": [
            "name",
            "domain",
            "email",
            "is_active",
            "-updated_at",
        ],
    }