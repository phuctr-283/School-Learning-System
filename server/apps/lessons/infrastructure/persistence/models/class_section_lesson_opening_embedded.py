from mongoengine import (
    EmbeddedDocument,
    ReferenceField,
    StringField,
    DateTimeField,
)

from apps.lessons.infrastructure.persistence.models.lesson_model import (
    LessonModel,
)


class ClassSectionLessonOpeningEmbedded(EmbeddedDocument):

    lesson = ReferenceField(
        LessonModel,
        required=True,
    )

    status = StringField(
        required=True,
        choices=[
            "locked",
            "open",
            "closed",
        ],
        default="locked",
    )

    opened_at = DateTimeField(
        null=True,
    )

    closed_at = DateTimeField(
        null=True,
    )
