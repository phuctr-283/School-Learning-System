from mongoengine import (
    Document,
    StringField,
    DateField,
    ReferenceField,
)

from apps.universities.infrastructure.persistence.models.university_model import UniversityModel


class AcademicYearModel(Document):

    meta = {
        "collection": "academic_years",
        "indexes": [
            "university",
            "name",
            "status",
            {
                "fields": [
                    "university",
                    "name",
                ],
                "unique": True,
            },
        ],
    }

    academic_year_id = StringField(
        required=True,
        max_length=30,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    name = StringField(
        required=True,
        max_length=20,
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
            "inactive",
        ],
        default="planned",
    )