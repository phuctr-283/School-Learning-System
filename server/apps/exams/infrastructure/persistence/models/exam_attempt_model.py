from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    EmbeddedDocumentListField,
    DecimalField,
    DateTimeField,
)

from .exam_attempt_answer_model import (
    ExamAttemptAnswerModel,
)


class ExamAttemptModel(
    Document
):

    meta = {
        "collection": "exam_attempts",

        "indexes": [
            "university",
            "exam",
            "exam_application",
            "student",
            "status",
            "-submitted_at",
        ],
    }

    # =========================================
    # IDENTIFICATION
    # =========================================

    exam_attempt_id = StringField(
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
    # APPLICATION
    # =========================================

    exam_application = ReferenceField(
        "ExamApplicationModel",
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
        ExamAttemptAnswerModel,
        default=list,
    )

    # =========================================
    # SCORE
    # =========================================

    total_score = DecimalField(
        required=True,
        precision=2,
        default=0.00,
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