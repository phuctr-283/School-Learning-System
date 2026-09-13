from mongoengine import (
    Document,
    StringField,
    DateField,
    ReferenceField,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)


class StudentModel(Document):

    meta = {
        "collection": "students",

        "indexes": [
            {
                "fields": [
                    "university",
                    "student_id",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "university",
                    "email",
                ],
                "unique": True,
                "sparse": True,
            },
            "university",
            "department",
            "student_class",
            "cohort_id",
            "status",
        ],
    }

    student_id = StringField(
        required=True,
        max_length=30,
    )

    full_name = StringField(
        required=True,
        max_length=255,
    )

    gender = StringField(
        required=True,
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
        required=False,
        null=True,
        max_length=255,
    )

    phone = StringField(
        required=False,
        null=True,
        max_length=20,
    )

    student_class = StringField(
        required=True,
        max_length=20,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    department = ReferenceField(
        DepartmentModel,
        required=True,
    )

    cohort_id = StringField(
        required=True,
        max_length=30,
    )

    status = StringField(
        required=True,
        choices=[
            "studying",
            "graduated",
            "reserved",
            "suspended",
            "dropped_out",
        ],
        default="studying",
    )