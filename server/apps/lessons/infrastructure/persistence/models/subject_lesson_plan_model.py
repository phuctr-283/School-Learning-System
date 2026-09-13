from mongoengine import (
    Document,
    IntField,
    StringField,
    BooleanField,
    ReferenceField,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class SubjectLessonPlanModel(Document):

    meta = {
        "collection": "subject_lesson_plans",

        "indexes": [
            {
                "fields": [
                    "university",
                    "subject_lesson_plan_id",
                ],
                "unique": True,
            },

            {
                "fields": [
                    "university",
                    "semester_number",
                    "lesson_type",
                    "min_credits",
                    "max_credits",
                ],
                "unique": True,
            },

            "university",
            "semester_number",
            "lesson_type",
        ],
    }

    subject_lesson_plan_id = StringField(
        required=True,
        max_length=30,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    semester_number = StringField(
        required=True,
        choices=[
            "1",
            "2",
            "3",
        ],
    )

    lesson_type = StringField(
        required=True,
        choices=[
            "theory",
            "practice",
        ],
    )

    min_credits = IntField(
        required=False,
        null=True,
        min_value=0,
    )

    max_credits = IntField(
        required=False,
        null=True,
        min_value=0,
    )

    total_lessons = IntField(
        required=True,
        min_value=1,
    )

    is_custom = BooleanField(
        default=True,
    )