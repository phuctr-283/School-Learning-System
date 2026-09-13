from mongoengine import (
    Document,
    StringField,
    DateField,
    ReferenceField,
)

from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)


class TeacherModel(Document):

    meta = {
        "collection": "teachers",
        "indexes": [
            "department",
            "status",
            "email",
            {
                "fields": [
                    "department",
                    "teacher_id",
                ],
                "unique": True,
            },
        ],
    }

    teacher_id = StringField(
        required=True,
        max_length=30,
    )

    full_name = StringField(
        required=True,
        max_length=255,
    )

    gender = StringField(
        required=False,
        null=True,
        choices=[
            "male",
            "female",
        ],
    )

    date_of_birth = DateField(
        required=False,
        null=True,
    )

    email = StringField(
        required=True,
        unique=True,
        max_length=255,
    )

    phone = StringField(
        required=False,
        null=True,
        max_length=20,
    )

    department = ReferenceField(
        "DepartmentModel",
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
