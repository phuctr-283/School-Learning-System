from mongoengine import (
    Document,
    StringField,
    IntField,
    ReferenceField,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.subjects.infrastructure.persistence.models.subject_model import (
    SubjectModel,
)

from apps.semesters.infrastructure.persistence.models.semester_model import (
    SemesterModel,
)


class CourseLessonPlanModel(Document):

    meta = {
        "collection": "course_lesson_plans",
        "indexes": [
            {
                "fields": [
                    "university",
                    "subject",
                    "semester",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "university",
                    "course_lesson_plan_id",
                ],
                "unique": True,
            },
            "university",
            "subject",
            "semester",
        ],
    }

    course_lesson_plan_id = StringField(
        required=True,
        max_length=30,
    )

    university = ReferenceField(
        UniversityModel,
        required=True,
    )

    subject = ReferenceField(
        SubjectModel,
        required=True,
    )

    semester = ReferenceField(
        SemesterModel,
        required=True,
    )

    total_lessons = IntField(
        required=True,
        min_value=1,
        max_value=100,
    )
