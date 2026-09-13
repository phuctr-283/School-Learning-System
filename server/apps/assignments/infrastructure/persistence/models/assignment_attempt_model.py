from decimal import Decimal
from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    EmbeddedDocumentListField,
    DecimalField,
    DateTimeField,
)

from .assignment_attempt_answer_model import (
    AssignmentAttemptAnswerModel,
)


class AssignmentAttemptModel(Document):

    meta = {
        "collection": "assignment_attempts",
        "indexes": [
            {
                "fields": [
                    "assignment_application",
                    "student",
                    "status",
                ],
            },
            "university",
            "assignment",
            "assignment_application",
            "student",
            "status",
            "-submitted_at",
        ],
    }

    # =========================================
    # IDENTIFICATION
    # =========================================

    assignment_attempt_id = StringField(
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
    # APPLICATION
    # =========================================

    assignment_application = ReferenceField(
        "AssignmentApplicationModel",
        required=True,
    )

    # =========================================
    # STUDENT
    # =========================================

    student = ReferenceField(
        "StudentModel",
        required=True,
    )

    # =========================================
    # ANSWERS
    # =========================================

    answers = EmbeddedDocumentListField(
        AssignmentAttemptAnswerModel,
        default=list,
    )

    # =========================================
    # SCORE
    # =========================================

    total_score = DecimalField(
        required=True,
        precision=2,
        default=Decimal("0.00"),
    )

    # =========================================
    # STATUS
    # =========================================

    status = StringField(
        required=True,
        choices=[
            "in_progress",
            "submitted",
            "graded",
        ],
        default="in_progress",
    )

    # =========================================
    # TIME
    # =========================================

    started_at = DateTimeField(
        required=True,
    )

    submitted_at = DateTimeField(
        required=False,
        null=True,
    )

    graded_at = DateTimeField(
        required=False,
        null=True,
    )
