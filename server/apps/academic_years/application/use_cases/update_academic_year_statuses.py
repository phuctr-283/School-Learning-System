from apps.academic_years.domain.services.academic_year_status_service import (
    AcademicYearStatusService,
)


class UpdateAcademicYearStatusesUseCase:

    def __init__(
        self,
        academic_year_repository,
    ):
        self.academic_year_repository = (
            academic_year_repository
        )

    def execute(
        self,
        university_id: str,
    ):

        academic_years = (
            self.academic_year_repository
            .get_by_university(
                university_id,
            )
        )

        updated_academic_years = []

        for academic_year in academic_years:

            new_status = (
                AcademicYearStatusService.calculate(
                    start_date=academic_year.start_date,
                    end_date=academic_year.end_date,
                )
            )

            if academic_year.status != new_status:

                academic_year = (
                    self.academic_year_repository
                    .update_status(
                        university_id=university_id,
                        academic_year_id=(
                            academic_year.academic_year_id
                        ),
                        status=new_status,
                    )
                )

            updated_academic_years.append(
                academic_year
            )

        return updated_academic_years