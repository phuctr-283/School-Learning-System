from apps.semesters.domain.services.semester_status_service import (
    SemesterStatusService,
)


class UpdateSemesterStatusesUseCase:

    def __init__(
        self,
        semester_repository,
    ):

        self.semester_repository = semester_repository

    def execute(
        self,
        university_id: str,
    ):

        semesters = self.semester_repository.get_by_university(
            university_id,
        )

        updated_semesters = []

        for semester in semesters:

            new_status = SemesterStatusService.calculate(
                start_date=semester.start_date,
                end_date=semester.end_date,
            )

            if semester.status != new_status:

                semester = self.semester_repository.update_status(
                    university_id=university_id,
                    semester_id=semester.semester_id,
                    status=new_status,
                )

            updated_semesters.append(semester)

        return updated_semesters
