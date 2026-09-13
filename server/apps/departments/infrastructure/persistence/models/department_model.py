from mongoengine import (
    Document,
    StringField,
    BooleanField,
    ReferenceField,
)


from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class DepartmentModel(Document):

    meta = {
        "collection": "departments",
        "indexes": [
            "university",
            "department_number",
            "name",
            "is_active",
            {
                "fields": [
                    "university",
                    "department_id",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "university",
                    "department_number",
                ],
                "unique": True,
            },
        ],
    }

    department_id = StringField(
        required=True,
        max_length=20,
    )

    department_number = StringField(
        required=True,
        max_length=10,
    )

    name = StringField(
        required=True,
        max_length=255,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    head = ReferenceField(
        "TeacherModel",
        required=False,
        null=True,
    )

    is_active = BooleanField(
        default=True,
    )
