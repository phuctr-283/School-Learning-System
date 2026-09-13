from mongoengine import (
    StringField,
)

from apps.assessment.infrastructure.persistence.models.assessment_model import (
    AssessmentModel,
)


class AssignmentModel(
    AssessmentModel
):

    meta = {
        "collection": "assignments",

        "indexes": [
            "university",
            "subject",
            "teacher",
            "status",
            "-created_at",
        ],
    }

    # =========================================
    # ASSIGNMENT ID
    # =========================================

    assignment_id = StringField(
        required=True,
        unique=True,
        max_length=100,
    )

    # =========================================
    # ASSIGNMENT TYPE
    # =========================================

    assignment_type = StringField(
        required=True,
        choices=[
            "practice",
            "homework",
            "quiz",
        ],
        default="practice",
    )