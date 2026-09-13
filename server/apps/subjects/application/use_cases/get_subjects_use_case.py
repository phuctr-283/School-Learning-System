from apps.subjects.application.dto.subject_dto import (
    SubjectDTO,
)


class GetSubjectsUseCase:

    def __init__(
        self,
        subject_repository,
    ):
        self.subject_repository = subject_repository

    def execute(
        self,
        university_id: str,
    ):
        subjects = self.subject_repository.get_by_university(
            university_id=university_id,
        )

        return [
            SubjectDTO(
                subject_id=subject.subject_id,
                name=subject.name,
                university_id=subject.university_id,
                university_name=subject.university_name,
                department_id=subject.department_id,
                department_name=subject.department_name,
                subject_types=subject.subject_types,
                credits=subject.credits,
                process_percent=subject.process_percent,
                midterm_percent=subject.midterm_percent,
                final_percent=subject.final_percent,
                status=subject.status,
            )
            for subject in subjects
        ]
