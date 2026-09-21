from datetime import datetime, timezone
from decimal import Decimal

from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)

from apps.assignments.application.dto.create_assignment_dto import (
    CreateAssignmentDTO,
)

from apps.assessment.application.services.question_parser_service import (
    QuestionParserService,
)


class CreateAssignmentUseCase:

    def __init__(
        self,
        assignment_repository,
        assignment_id_generator,
        subject_repository,
    ):
        self.assignment_repository = assignment_repository

        self.assignment_id_generator = assignment_id_generator

        self.subject_repository = subject_repository

    def execute(
        self,
        dto: CreateAssignmentDTO,
        university_id: str,
        teacher_email: str,
    ):

        title = (dto.title or "").strip()

        if not title:
            raise ValueError("Tên bài tập không được để trống.")

        subject_id = (dto.subject_id or "").strip()

        if not subject_id:
            raise ValueError("Chưa chọn môn học.")

        if dto.assignment_type not in {
            "practice",
            "homework",
            "quiz",
        }:
            raise ValueError("Loại bài tập không hợp lệ.")

        if dto.duration_minutes < 1 or dto.duration_minutes > 600:
            raise ValueError("Thời gian làm bài " "phải từ 1 đến 600 phút.")

        subject = self.subject_repository.get_by_id(
            subject_id=subject_id,
            university_id=university_id,
        )

        if subject is None:
            raise ValueError("Không tìm thấy môn học " "thuộc trường đại học.")

        department_id = str(
            subject.department_id,
        )

        questions = QuestionParserService.parse_questions(
            dto.questions,
        )

        now = datetime.now(
            timezone.utc,
        )

        assignment = Assignment(
            assignment_id=(self.assignment_id_generator.generate()),
            university_id=university_id,
            department_id=department_id,
            subject_id=subject_id,
            teacher_id="",
            title=title,
            description=(dto.description or None),
            assignment_type=dto.assignment_type,
            questions=questions,
            total_score=Decimal("10.00"),
            duration_minutes=dto.duration_minutes,
            status="published",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return self.assignment_repository.create_by_teacher_email(
            assignment=assignment,
            teacher_email=teacher_email,
        )
