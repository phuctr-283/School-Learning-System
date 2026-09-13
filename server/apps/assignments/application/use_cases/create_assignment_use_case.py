from decimal import Decimal
from django.utils import timezone
import secrets
import string

from apps.assignments.application.dto.create_assignment_dto import (
    CreateAssignmentDTO,
)

from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)

from apps.assessment.application.services.question_parser_service import (
    QuestionParserService,
)


class CreateAssignmentUseCase:

    def __init__(
        self,
        assignment_repository,
        university_repository,
        department_repository,
        subject_repository,
        teacher_repository,
    ):

        self.assignment_repository = assignment_repository
        self.university_repository = university_repository
        self.department_repository = department_repository
        self.subject_repository = subject_repository
        self.teacher_repository = teacher_repository

    def execute(
        self,
        dto: CreateAssignmentDTO,
    ) -> Assignment:

        university_id = dto.university_id.strip().upper()
        department_id = dto.department_id.strip().upper()
        subject_id = dto.subject_id.strip().upper()
        teacher_id = dto.teacher_id.strip().upper()
        title = (dto.title or "").strip()

        if not title:
            raise ValueError(
                "Tiêu đề bài tập không được để trống."
            )

        # =================================================
        # UNIVERSITY
        # =================================================

        university = self.university_repository.get_by_id(
            university_id,
        )

        if university is None:
            raise ValueError(
                "Không tìm thấy trường đại học."
            )

        # =================================================
        # DEPARTMENT
        # =================================================

        department = self.department_repository.get_by_id(
            department_id=department_id,
            university_id=university_id,
        )

        if department is None:
            raise ValueError(
                "Không tìm thấy khoa thuộc trường đại học."
            )

        # =================================================
        # SUBJECT
        # =================================================

        subject = self.subject_repository.get_by_id(
            subject_id=subject_id,
            university_id=university_id,
        )

        if subject is None:
            raise ValueError(
                "Môn học không tồn tại trong trường."
            )

        # =================================================
        # TEACHER
        # =================================================

        teacher = self.teacher_repository.get_by_id(
            teacher_id=teacher_id,
            university_id=university_id,
            department_id=department_id,
        )

        if teacher is None:
            raise ValueError(
                "Không tìm thấy giảng viên thuộc khoa."
            )

        # =================================================
        # PARSE QUESTIONS
        # =================================================

        question_entities = (
            QuestionParserService.parse_questions(
                raw_questions=dto.questions,
            )
        )

        # =================================================
        # CREATE ASSIGNMENT
        # =================================================

        now = timezone.now()

        assignment = Assignment(
            assignment_id=self.generate_assignment_id(
                university_id=university_id,
                department_number=department.department_number,
            ),
            university_id=university_id,
            department_id=department_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            title=title,
            description=(
                dto.description.strip()
                if dto.description
                and dto.description.strip()
                else None
            ),
            questions=question_entities,
            total_score=Decimal("10.00"),
            assignment_type=dto.assignment_type,
            status="draft",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return self.assignment_repository.create(
            assignment,
        )

    @staticmethod
    def generate_assignment_id(
        university_id: str,
        department_number,
    ) -> str:

        random_part = "".join(
            secrets.choice(
                string.ascii_uppercase + string.digits
            )
            for _ in range(16)
        )

        department_code = str(
            department_number
        ).strip().zfill(2)

        return (
            f"ASG-"
            f"{university_id}-"
            f"{department_code}-"
            f"{random_part}"
        )