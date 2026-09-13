from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)

from apps.assignments.infrastructure.persistence.models.assignment_model import (
    AssignmentModel,
)

from apps.assessment.infrastructure.persistence.mappers.assessment_question_mapper import (
    AssessmentQuestionMapper,
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
            AssessmentQuestionMapper.to_model(
                question,
            )
            for question in entity.questions
        ]

        return AssignmentModel(
            assignment_id=entity.assignment_id,
            title=entity.title,
            description=entity.description,
            university=university,
            subject=subject,
            teacher=teacher,
            questions=question_models,
            total_score=entity.total_score,
            assignment_type=entity.assignment_type,
            status=entity.status,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(
        model: AssignmentModel,
    ) -> Assignment:

        questions = [
            AssessmentQuestionMapper.to_entity(
                question_model,
            )
            for question_model in (
                model.questions or []
            )
        ]

        return Assignment(
            assignment_id=model.assignment_id,
            university_id=(
                model.university.university_id
            ),
            department_id=(
                model.teacher.department.department_id
            ),
            subject_id=model.subject.subject_id,
            teacher_id=model.teacher.teacher_id,
            title=model.title,
            description=model.description,
            questions=questions,
            total_score=model.total_score,
            assignment_type=model.assignment_type,
            status=model.status,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )