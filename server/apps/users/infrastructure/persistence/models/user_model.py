from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    BooleanField,
    IntField,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)
from django.utils import timezone

class UserModel(Document):

    user_id = StringField(
        required=True,
        primary_key=True,
        max_length=50,
    )
    username = StringField(
        required=True,
        max_length=100,
    )
    password = StringField(
        required=True,
    )
    account_level = IntField(
        required=True,
        choices=[
            level.value
            for level in AccountLevel
        ],
    )
    university_id = StringField(
        null=True,
        max_length=50,
    )
    last_login = DateTimeField(
        null=True,
    )
    is_login = BooleanField(
        default=False,
    )
    is_active = BooleanField(
        default=True,
    )
    created_at = DateTimeField(
        required=True,
    )
    updated_at = DateTimeField(
        required=True,
    )
    meta = {
        "collection": "users",
        "indexes": [
            "username",
            "account_level",
            "university_id",
            "is_active",
            "is_login",
            "-updated_at",
        ],
    }