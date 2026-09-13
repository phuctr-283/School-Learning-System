from mongoengine import (
    Document,
    StringField,
    IntField,
    ReferenceField,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class LessonModel(Document):

    meta = {
        "collection": "lessons",
        "indexes": [
            {
                "fields": [
                    "university",
                    "lesson_id",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "university",
                    "lesson_number",
                ],
                "unique": True,
            },
            "university",
        ],
    }

    lesson_id = StringField(
        required=True,
        max_length=30,
    )

    lesson_number = IntField(
        required=True,
        min_value=1,
    )

    name = StringField(
        required=True,
        max_length=100,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )
