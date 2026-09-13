from mongoengine import (
    Document,
    StringField,
    IntField,
    ReferenceField,
)


from apps.semesters.infrastructure.persistence.models.semester_model import (
    SemesterModel,
)


from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class SemesterLessonPlanModel(Document):

    meta = {

        "collection": "semester_lesson_plans",

        "indexes": [


            {
                "fields": [
                    "university",
                    "semester_lesson_plan_id",
                ],
                "unique": True,
            },
            {
                "fields": [
                    "university",
                    "semester",
                ],
                "unique": True,
            },

            "university",
            "semester",
        ],
    }


    semester_lesson_plan_id = StringField(
        required=True,
        max_length=30,
    )


    university = ReferenceField(
        UniversityModel,
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