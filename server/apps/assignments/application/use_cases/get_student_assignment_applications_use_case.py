from apps.assignments.application.dto.assignment_application_content_dto import (
    AssignmentApplicationDTO,
)


class GetStudentAssignmentApplicationsUseCase:

    def __init__(
        self,
        assignment_application_repository,
    ):
        self.assignment_application_repository = assignment_application_repository

    def execute(
        self,
        university_id: str,
        student_id: str,
        class_section_id: str,
        lesson_id: str,
    ):
        applications = (
            self.assignment_application_repository.get_student_assignment_applications(
                university_id=university_id,
                student_id=student_id,
                class_section_id=class_section_id,
                lesson_id=lesson_id,
            )
        )

        result = []

        for (
            application,
            class_section_application,
        ) in applications:

            assignment = application.assignment
            subject = assignment.subject
            class_section = class_section_application.class_section

            result.append(
                AssignmentApplicationDTO(
                    assignment_application_id=(application.assignment_application_id),
                    assignment_id=(assignment.assignment_id),
                    university_id=str(application.university.university_id),
                    lesson_id=application.lesson_id,
                    class_section_id=(class_section.class_section_id),
                    class_section_status=(class_section_application.status),
                    class_section_opened_at=(class_section_application.opened_at),
                    class_section_closed_at=(class_section_application.closed_at),
                    title=assignment.title,
                    description=assignment.description,
                    subject_id=subject.subject_id,
                    subject_name=subject.name,
                    assignment_type=(assignment.assignment_type),
                    total_score=assignment.total_score,
                    duration_minutes=(assignment.duration_minutes),
                    status=application.status,
                    max_attempts=application.max_attempts,
                    open_at=application.open_at,
                    due_at=application.due_at,
                    created_at=application.created_at,
                    updated_at=application.updated_at,
                )
            )

        return result
