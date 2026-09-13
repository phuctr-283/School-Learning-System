from mongoengine import (
    Document,
    StringField,
    DateField,
    ReferenceField,
)
from apps.academic_years.infrastructure.persistence.models.academic_year_model import (
    AcademicYearModel,
)


class SemesterModel(Document):

    meta = {
        "collection": "semesters",
        "indexes": [
            "academic_year",
            "status",
            {
                "fields": [
                    "academic_year",
                    "semester_number",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "academic_year",
                    "semester_id",
                ],
                "unique": True,
            },
        ],
    }

    semester_id = StringField(
        required=True,
        max_length=30,
    )

    name = StringField(
        required=True,
        max_length=100,
    )

    semester_number = StringField(
        required=True,
        choices=[
            "1",
            "2",
            "3",
        ],
    )

    academic_year = ReferenceField(
        AcademicYearModel,
        required=True,
    )

    start_date = DateField(
        required=True,
    )

    end_date = DateField(
        required=True,
    )

    status = StringField(
        required=True,
        choices=[
            "planned",
            "active",
            "locked",
        ],
        default="planned",
    )
