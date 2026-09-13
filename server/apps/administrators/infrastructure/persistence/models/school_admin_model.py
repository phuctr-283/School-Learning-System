from mongoengine import (
    Document,
    StringField,
    EmailField,
    ReferenceField,
)
from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class SchoolAdminModel(Document):

    meta = {
        "collection": "school-admins",
        "indexes": [
            "university",
            "email",
            "status",
        ],
    }

    school_admin_id = StringField(
        primary_key=True,
        required=True,
        max_length=30,
    )

    full_name = StringField(
        required=True,
        max_length=100,
    )

    gender = StringField(
        required=False,
        null=True,
        choices=[
            "male",
            "female",
        ],
    )

    email = EmailField(
        required=True,
        unique=True,
    )

    phone = StringField(
        required=False,
        unique=True,
        sparse=True,
        max_length=20,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    status = StringField(
        required=True,
        choices=[
            "active",
            "inactive",
        ],
        default="active",
    )
