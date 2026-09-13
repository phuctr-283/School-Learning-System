from decimal import Decimal
from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    EmbeddedDocumentListField,
    DecimalField,
    BooleanField,
    DateTimeField,
)

from .assessment_question_model import (
    AssessmentQuestionModel,
)


class AssessmentModel(
    Document
):

    meta = {
        "abstract": True,
    }

    # =========================================
    # BASIC INFORMATION
    # =========================================

    title = StringField(
        required=True,
        max_length=255,
    )

    description = StringField(
        required=False,
        null=True,
    )

    # =========================================
    # OWNER
    # =========================================

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

    # =========================================
    # QUESTIONS
    # =========================================

    questions = EmbeddedDocumentListField(
        AssessmentQuestionModel,
        required=True,
    )

    # =========================================
    # SCORE
    # =========================================

    total_score = DecimalField(
    required=True,
    precision=2,
    default=Decimal("10.00"),
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

    is_active = BooleanField(
        default=True,
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