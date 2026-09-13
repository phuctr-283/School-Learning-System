from mongoengine import (
    Document,
    StringField,
    IntField,
    DecimalField,
    ReferenceField,
    ListField,
)
from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)
from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)


class SubjectModel(Document):

    meta = {
        "collection": "subjects",
        "indexes": [
            "department",
            "name",
            "status",
            "university",
            {
                "fields": [
                    "department",
                    "subject_id",
                ],
                "unique": True,
            },
        ],
    }

    subject_id = StringField(
        required=True,
        max_length=30,
    )

    name = StringField(
        required=True,
        max_length=255,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    department = ReferenceField(
        DepartmentModel,
        required=True,
    )

    subject_types = StringField(
        required=True,
        choices=[
            "Theory",
            "Practice",
        ],
    )

    credits = IntField(
        required=True,
        min_value=1,
    )

    process_percent = DecimalField(
        required=True,
        precision=2,
        min_value=0,
        max_value=100,
    )

    midterm_percent = DecimalField(
        required=True,
        precision=2,
        min_value=0,
        max_value=100,
    )

    final_percent = DecimalField(
        required=True,
        precision=2,
        min_value=0,
        max_value=100,
    )

    status = StringField(
        required=True,
        choices=[
            "active",
            "inactive",
        ],
        default="active",
    )
