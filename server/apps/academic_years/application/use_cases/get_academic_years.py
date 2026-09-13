from apps.academic_years.application.dto.academic_year_dto import (
    AcademicYearDTO,
)


class GetAcademicYearsUseCase:

    def __init__(
        self,
        academic_year_repository,
        update_academic_year_statuses_use_case,
    ):

        self.academic_year_repository = academic_year_repository

        self.update_academic_year_statuses_use_case = (
            update_academic_year_statuses_use_case
        )

    def execute(
        self,
        university_id: str,
    ):

        academic_years = self.update_academic_year_statuses_use_case.execute(
            university_id=university_id,
        )

        return [
            AcademicYearDTO(
                academic_year_id=(academic_year.academic_year_id),
                university_id=(academic_year.university_id),
                university_name=(academic_year.university_name),
                name=academic_year.name,
                start_date=(academic_year.start_date),
                end_date=(academic_year.end_date),
                status=academic_year.status,
            )
            for academic_year in academic_years
        ]
