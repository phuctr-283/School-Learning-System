from mongoengine import (
    Document,
    ReferenceField,
    EmbeddedDocumentListField,
    StringField,
    DateTimeField,
    IntField,
)
from apps.assignments.infrastructure.persistence.models.assignment_application_class_section_model import AssignmentApplicationClassSectionModel
class AssignmentApplicationModel(Document):

    meta = {
        "collection": "assignment_applications",

        "indexes": [
            {
                "fields": [
                    "assignment",
                    "lesson_id",
                ],
                "unique": True,
            },

            "university",
            "assignment",
            "class_sections.class_section",
            "class_sections.status",
            "lesson_id",
            "status",
            "open_at",
            "due_at",
        ],
    }

    assignment_application_id = StringField(
        required=True,
        unique=True,
        max_length=30,
    )

    university = ReferenceField(
        "UniversityModel",
        required=True,
    )

    assignment = ReferenceField(
        "AssignmentModel",
        required=True,
    )

    class_sections = EmbeddedDocumentListField(
        AssignmentApplicationClassSectionModel,
        default=list,
    )

    lesson_id = StringField(
        required=True,
        max_length=100,
    )

    status = StringField(
        required=True,
        choices=[
            "draft",
            "published",
            "closed",
        ],
        default="draft",
    )

    open_at = DateTimeField(
        required=False,
        null=True,
    )

    due_at = DateTimeField(
        required=False,
        null=True,
    )

    max_attempts = IntField(
        required=True,
        min_value=1,
        default=1,
    )

    created_at = DateTimeField(
        required=True,
    )

    updated_at = DateTimeField(
        required=True,
    )