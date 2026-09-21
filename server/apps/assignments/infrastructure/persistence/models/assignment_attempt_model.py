from datetime import datetime, timezone

from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField,
    DictField,
    DecimalField,
    IntField,
)

from apps.students.infrastructure.persistence.models.student_model import (
    StudentModel,
)

from apps.assignments.infrastructure.persistence.models.assignment_application_model import (
    AssignmentApplicationModel,
)

from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)


class AssignmentAttemptModel(Document):

    meta = {
        "collection": "assignment_attempts",
        "indexes": [
            "attempt_id",
            "assignment_application",
            "student",
            "class_section",
            "status",
            "-started_at",
            "-submitted_at",
        ],
    }

    attempt_id = StringField(
        required=True,
        unique=True,
        max_length=50,
    )

    assignment_application = ReferenceField(
        AssignmentApplicationModel,
        required=True,
    )

    student = ReferenceField(
        StudentModel,
        required=True,
    )

    class_section = ReferenceField(
        ClassSectionModel,
        required=True,
    )

    status = StringField(
        choices=[
            "in_progress",
            "submitted",
            "graded",
        ],
        default="in_progress",
    )

    started_at = DateTimeField(
        required=True,
    )

    submitted_at = DateTimeField(
        null=True,
    )

    answers = DictField(
        default=dict,
    )

    score = DecimalField(
        precision=2,
        force_string=False,
        null=True,
    )

    total_score = DecimalField(
        precision=2,
        force_string=False,
        null=True,
    )

    answered_count = IntField(
        default=0,
    )

    created_at = DateTimeField(
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = DateTimeField(
        default=lambda: datetime.now(timezone.utc),
    )