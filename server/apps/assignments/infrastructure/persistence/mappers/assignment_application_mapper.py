from decimal import Decimal

from apps.assignments.application.dto.assignment_application_content_dto import (
    AssignmentApplicationClassSectionDTO,
    AssignmentApplicationContentDTO,
)


class AssignmentApplicationMapper:

    @staticmethod
    def to_content_dto(
        model,
    ) -> AssignmentApplicationContentDTO:

        assignment = model.assignment
        university = model.university
        subject = assignment.subject

        class_sections = [
            AssignmentApplicationClassSectionDTO(
                class_section_id=str(item.class_section.class_section_id),
                status=item.status,
                opened_at=item.opened_at,
                closed_at=item.closed_at,
            )
            for item in (model.class_sections or [])
        ]

        return AssignmentApplicationContentDTO(
            assignment_application_id=str(model.assignment_application_id),
            assignment_id=str(assignment.assignment_id),
            university_id=str(university.university_id),
            lesson_id=str(model.lesson_id),
            class_sections=class_sections,
            title=assignment.title,
            description=assignment.description,
            subject_id=str(subject.subject_id),
            subject_name=subject.name,
            assignment_type=assignment.assignment_type,
            total_score=Decimal(str(assignment.total_score)),
            duration_minutes=assignment.duration_minutes,
            status=model.status,
            max_attempts=model.max_attempts,
            open_at=model.open_at,
            due_at=model.due_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
