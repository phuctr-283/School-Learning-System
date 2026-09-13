from mongoengine import (
    Document,
    StringField,
    DateTimeField,
)


class RevokedTokenModel(Document):

    jti = StringField(
        required=True,
        unique=True,
    )
    user_id = StringField(
        required=True,
    )
    expires_at = DateTimeField(
        required=True,
    )
    revoked_at = DateTimeField(
        required=True,
    )
    meta = {
        "collection": "revoked_tokens",
        "indexes": [
            {
                "fields": ["expires_at"],
                "expireAfterSeconds": 0,
            }
        ],
    }
