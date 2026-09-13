from mongoengine import (
    Document,
    ReferenceField,
)


class ClassSectionStudentModel(Document):

    meta = {
        "collection": "class_section_students",

        "indexes": [
            {
                "fields": [
                    "class_section",
                    "student",
                ],
                "unique": True,
            },
            "class_section",
            "student",
        ],
    }

    class_section = ReferenceField(
        "ClassSectionModel",
        required=True,
    )

    student = ReferenceField(
        "StudentModel",
        required=True,
    )