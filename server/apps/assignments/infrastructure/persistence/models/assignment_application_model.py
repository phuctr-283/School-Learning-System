from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DateTimeField,
    IntField,
)


class AssignmentApplicationModel(
    Document
):

    meta = {
        "collection": "assignment_applications",

        "indexes": [
            {
                "fields": [
                    "assignment",
                    "class_section",
                    "lesson_opening",
                ],
                "unique": True,
            },

            "university",
            "assignment",
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

    assignment_application_id = StringField(
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
    # ASSIGNMENT
    # =========================================

    assignment = ReferenceField(
        "AssignmentModel",
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
    # ATTEMPTS
    # =========================================

    max_attempts = IntField(
        required=True,
        min_value=1,
        default=1,
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