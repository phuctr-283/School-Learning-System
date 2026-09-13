from mongoengine import (
    Document,
    StringField,
    IntField,
    ReferenceField,
)


class SubjectScheduleModel(Document):

    meta = {
        "collection": "subject_schedules",

        "indexes": [
            {
                "fields": [
                    "subject",
                    "subject_type",
                    "lesson_number",
                ],
                "unique": True,
            },
            "subject",
            "subject_type",
            "lesson_number",
        ],
    }

    subject_schedule_id = StringField(
        primary_key=True,
        required=True,
        max_length=30,
    )

    subject = ReferenceField(
        "SubjectModel",
        required=True,
    )

    subject_type = ReferenceField(
        "SubjectTypeModel",
        required=True,
    )

    lesson_number = IntField(
        required=True,
        min_value=1,
    )