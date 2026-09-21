from decimal import Decimal

from apps.assignments.application.dto.assignment_content_dto import (
    AssignmentContentDTO,
)

from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)

from apps.assessment.infrastructure.persistence.mappers.assessment_question_mapper import (
    AssessmentQuestionMapper,
)

from apps.assignments.infrastructure.persistence.models.assignment_model import (
    AssignmentModel,
)


class AssignmentMapper:

    @staticmethod
    def to_model(
        entity: Assignment,
        university,
        subject,
        teacher,
    ) -> AssignmentModel:

        question_models = [
            AssessmentQuestionMapper.to_model(question) for question in entity.questions
        ]

        return AssignmentModel(
            assignment_id=entity.assignment_id,
            title=entity.title,
            description=entity.description,
            university=university,
            subject=subject,
            teacher=teacher,
            assignment_type=entity.assignment_type,
            questions=question_models,
            total_score=entity.total_score,
            duration_minutes=entity.duration_minutes,
            status=entity.status,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(
        model: AssignmentModel,
    ) -> Assignment:

        subject = model.subject
        teacher = model.teacher
        university = model.university

        if subject is None:
            raise ValueError(
                "Bài tập chưa được gán môn học.",
            )

        if subject.department is None:
            raise ValueError(
                "Môn học của bài tập chưa được gán khoa.",
            )

        if teacher is None:
            raise ValueError(
                "Bài tập chưa được gán giảng viên.",
            )

        if university is None:
            raise ValueError(
                "Bài tập chưa được gán trường đại học.",
            )

        return Assignment(
            assignment_id=str(model.assignment_id),
            university_id=str(university.university_id),
            department_id=str(subject.department.department_id),
            subject_id=str(subject.subject_id),
            teacher_id=str(teacher.teacher_id),
            title=model.title,
            description=model.description,
            assignment_type=model.assignment_type,
            questions=[
                AssessmentQuestionMapper.to_entity(question)
                for question in model.questions
            ],
            total_score=model.total_score,
            duration_minutes=model.duration_minutes,
            status=model.status,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_content_dto(
        model: AssignmentModel,
    ) -> AssignmentContentDTO:

        subject = model.subject
        teacher = model.teacher
        university = model.university

        if subject is None:
            raise ValueError(
                "Bài tập chưa được gán môn học.",
            )

        if teacher is None:
            raise ValueError(
                "Bài tập chưa được gán giảng viên.",
            )

        if university is None:
            raise ValueError(
                "Bài tập chưa được gán trường đại học.",
            )

        return AssignmentContentDTO(
            assignment_id=str(model.assignment_id),
            university_id=str(university.university_id),
            subject_id=str(subject.subject_id),
            subject_name=subject.name,
            teacher_id=str(teacher.teacher_id),
            title=model.title,
            description=model.description,
            assignment_type=str(model.assignment_type),
            total_score=Decimal(str(model.total_score)),
            duration_minutes=model.duration_minutes,
            status=str(model.status),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
