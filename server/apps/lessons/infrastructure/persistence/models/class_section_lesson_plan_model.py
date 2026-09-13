from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    ReferenceField,
)

from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.lessons.infrastructure.persistence.models.course_lesson_plan_model import (
    CourseLessonPlanModel,
)


class ClassSectionLessonPlanModel(Document):

    meta = {
        "collection": "class_section_lesson_plans",

        "indexes": [

            {
                "fields": [
                    "university",
                    "class_section_lesson_plan_id",
                ],
                "unique": True,
            },

            {
                "fields": [
                    "university",
                    "class_section",
                ],
                "unique": True,
            },

            "university",
            "class_section",
            "course_lesson_plan",
        ],
    }

    class_section_lesson_plan_id = StringField(
        required=True,
        max_length=30,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    class_section = ReferenceField(
        ClassSectionModel,
        required=True,
    )

    course_lesson_plan = ReferenceField(
        CourseLessonPlanModel,
        required=True,
    )

    is_custom = BooleanField(
        default=False,
    )

    custom_total_lessons = IntField(
        required=False,
        null=True,
        min_value=1,
        max_value=100,
    )