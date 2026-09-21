from mongoengine import (
    EmbeddedDocument,
    ReferenceField,
    StringField,
    DateTimeField,
)


class AssignmentApplicationClassSectionModel(
    EmbeddedDocument
):
    class_section = ReferenceField(
        "ClassSectionModel",
        required=True,
    )

    status = StringField(
        required=True,
        choices=[
            "active",
            "closed",
        ],
        default="closed",
    )

    opened_at = DateTimeField(
        required=False,
        null=True,
    )

    closed_at = DateTimeField(
        required=False,
        null=True,
    )