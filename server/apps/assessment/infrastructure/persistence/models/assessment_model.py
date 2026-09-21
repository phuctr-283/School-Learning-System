from decimal import Decimal
from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    EmbeddedDocumentListField,
    DecimalField,
    BooleanField,
    DateTimeField,
    IntField,
)

from .assessment_question_model import (
    AssessmentQuestionModel,
)


class AssessmentModel(Document):

    meta = {
        "abstract": True,
    }

    title = StringField(
        required=True,
        max_length=255,
    )

    description = StringField(
        required=False,
        null=True,
    )

    university = ReferenceField(
        "UniversityModel",
        required=True,
    )

    subject = ReferenceField(
        "SubjectModel",
        required=True,
    )

    teacher = ReferenceField(
        "TeacherModel",
        required=True,
    )

    questions = EmbeddedDocumentListField(
        AssessmentQuestionModel,
        required=True,
    )

    total_score = DecimalField(
        required=True,
        precision=2,
        default=Decimal("10.00"),
    )
    duration_minutes = IntField(
        required=True,
        min_value=1,
        default=30,
    )

    status = StringField(
        required=True,
        choices=[
            "draft",
            "published",
            "closed",
        ],
        default="published",
    )

    is_active = BooleanField(
        default=True,
    )

    created_at = DateTimeField(
        required=True,
    )

    updated_at = DateTimeField(
        required=True,
    )
