from mongoengine import (
    StringField,
)

from apps.assessment.infrastructure.persistence.models.assessment_model import (
    AssessmentModel,
)


class ExamModel(
    AssessmentModel
):

    meta = {
        "collection": "exams",

        "indexes": [
            "university",
            "subject",
            "teacher",
            "exam_type",
            "status",
            "-created_at",
        ],
    }

    # =========================================
    # EXAM ID
    # =========================================

    exam_id = StringField(
        required=True,
        unique=True,
        max_length=30,
    )

    # =========================================
    # EXAM TYPE
    # =========================================

    exam_type = StringField(
        required=True,
        choices=[
            "midterm",
            "final",
        ],
    )