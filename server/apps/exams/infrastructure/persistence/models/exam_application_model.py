from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DateTimeField,
)


class ExamApplicationModel(
    Document
):

    meta = {
        "collection": "exam_applications",

        "indexes": [
            {
                "fields": [
                    "exam",
                    "class_section",
                ],
                "unique": True,
            },

            "university",
            "exam",
            "class_section",
            "lesson_opening",
            "status",
            "open_at",
            "due_at",
        ],
    }

    # =========================================
    # IDENTIFICATION
    # =========================================

    exam_application_id = StringField(
        required=True,
        unique=True,
        max_length=30,
    )

    # =========================================
    # UNIVERSITY
    # =========================================

    university = ReferenceField(
        "UniversityModel",
        required=True,
    )

    # =========================================
    # EXAM
    # =========================================

    exam = ReferenceField(
        "ExamModel",
        required=True,
    )

    # =========================================
    # CLASS SECTION
    # =========================================

    class_section = ReferenceField(
        "ClassSectionModel",
        required=True,
    )

    # =========================================
    # LESSON OPENING
    # =========================================

    lesson_opening = ReferenceField(
        "LessonOpeningModel",
        required=False,
        null=True,
    )

    # =========================================
    # STATUS
    # =========================================

    status = StringField(
        required=True,
        choices=[
            "draft",
            "published",
            "closed",
        ],
        default="draft",
    )

    # =========================================
    # TIME
    # =========================================

    open_at = DateTimeField(
        required=False,
        null=True,
    )

    due_at = DateTimeField(
        required=False,
        null=True,
    )

    # =========================================
    # TIMESTAMP
    # =========================================

    created_at = DateTimeField(
        required=True,
    )

    updated_at = DateTimeField(
        required=True,
    )