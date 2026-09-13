from apps.semesters.application.dto.semester_dto import (
    SemesterDTO,
)


class GetSemestersUseCase:

    def __init__(
        self,
        semester_repository,
        update_semester_statuses_use_case,
    ):

        self.semester_repository = semester_repository

        self.update_semester_statuses_use_case = update_semester_statuses_use_case

    def execute(
        self,
        university_id: str,
    ):

        semesters = self.update_semester_statuses_use_case.execute(
            university_id=university_id,
        )

        return [
            SemesterDTO(
                semester_id=semester.semester_id,
                name=semester.name,
                semester_number=(semester.semester_number),
                academic_year_id=(semester.academic_year_id),
                academic_year_name=(semester.academic_year_name),
                university_id=(semester.university_id),
                university_name=(semester.university_name),
                start_date=semester.start_date,
                end_date=semester.end_date,
                status=semester.status,
            )
            for semester in semesters
        ]
