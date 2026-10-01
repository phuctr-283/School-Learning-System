from datetime import datetime, timezone
from decimal import Decimal

from apps.assignments.application.dto.update_assignment_dto import (
    UpdateAssignmentDTO,
)

from apps.assessment.application.services.question_parser_service import (
    QuestionParserService,
)


class UpdateAssignmentUseCase:

    def __init__(
        self,
        assignment_repository,
        subject_repository,
    ):
        self.assignment_repository = assignment_repository
        self.subject_repository = subject_repository

    def execute(
        self,
        assignment_id: str,
        dto: UpdateAssignmentDTO,
        university_id: str,
        teacher_email: str,
    ):

        assignment_id = (assignment_id or "").strip()

        if not assignment_id:
            raise ValueError(
                "Thiếu mã bài tập.",
            )

        title = (dto.title or "").strip()

        if not title:
            raise ValueError(
                "Tên bài tập không được để trống.",
            )

        subject_id = (dto.subject_id or "").strip()

        if not subject_id:
            raise ValueError(
                "Chưa chọn môn học.",
            )

        if dto.assignment_type not in {
            "practice",
            "homework",
            "quiz",
        }:
            raise ValueError(
                "Loại bài tập không hợp lệ.",
            )

        if dto.duration_minutes < 1 or dto.duration_minutes > 600:
            raise ValueError(
                "Thời gian làm bài " "phải từ 1 đến 600 phút.",
            )

        # =========================================
        # SUBJECT
        # =========================================

        subject = self.subject_repository.get_by_id(
            subject_id=subject_id,
            university_id=university_id,
        )

        if subject is None:
            raise ValueError(
                "Không tìm thấy môn học " "thuộc trường đại học.",
            )

        department_id = str(
            subject.department_id,
        )

        # =========================================
        # QUESTIONS
        # =========================================

        questions = QuestionParserService.parse_questions(
            dto.questions,
        )

        # =========================================
        # UPDATE
        # =========================================

        now = datetime.now(
            timezone.utc,
        )

        return self.assignment_repository.update_by_teacher_email(
            assignment_id=assignment_id,
            university_id=university_id,
            teacher_email=teacher_email,
            subject_id=subject_id,
            department_id=department_id,
            title=title,
            description=(dto.description.strip() if dto.description else None),
            assignment_type=dto.assignment_type,
            questions=questions,
            duration_minutes=dto.duration_minutes,
            updated_at=now,
        )
