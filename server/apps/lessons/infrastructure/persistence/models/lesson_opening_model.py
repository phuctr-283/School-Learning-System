from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    IntField,
    DateTimeField,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.lessons.infrastructure.persistence.models.lesson_model import (
    LessonModel,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_plan_model import (
    ClassSectionLessonPlanModel,
)

class LessonOpeningModel(Document):

    meta = {
        "collection": "lesson_openings",

        "indexes": [
            {
                "fields": [
                    "university",
                    "lesson_opening_id",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "university",
                    "class_section_lesson_plan",
                    "lesson",
                ],
                "unique": True,
            },
            "university",
            "class_section_lesson_plan",
            "lesson",
            "status",
            "-opened_at",
        ],
    }

    lesson_opening_id = StringField(
        required=True,
        max_length=30,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    class_section_lesson_plan = ReferenceField(
        ClassSectionLessonPlanModel,
        required=True,
    )

    lesson = ReferenceField(
        LessonModel,
        required=True,
    )

    status = StringField(
        required=True,
        choices=[
            "locked",
            "open",
            "closed",
        ],
        default="locked",
    )

    opened_at = DateTimeField(
        null=True,
    )

    closed_at = DateTimeField(
        null=True,
    )

    created_at = DateTimeField(
        required=True,
    )

    updated_at = DateTimeField(
        required=True,
    )