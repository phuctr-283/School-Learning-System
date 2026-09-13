from mongoengine import (
    Document,
    ReferenceField,
)


class ClassSectionLessonModel(Document):

    meta = {
        "collection": "class_section_lessons",

        "indexes": [
            {
                "fields": [
                    "class_section",
                    "lesson_slot",
                ],
                "unique": True,
            },
            "class_section",
            "lesson_slot",
        ],
    }

    class_section = ReferenceField(
        "ClassSectionModel",
        required=True,
    )

    lesson_slot = ReferenceField(
        "LessonSlotModel",
        required=True,
    )