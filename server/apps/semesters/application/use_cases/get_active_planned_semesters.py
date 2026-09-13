from apps.semesters.application.dto.semester_content_dto import (
    SemesterContentDTO,
)

from apps.semesters.domain.repositories.semester_repository import (
    SemesterRepository,
)


class GetActivePlannedSemestersUseCase:

    def __init__(
        self,
        semester_repository: SemesterRepository,
    ):
        self.semester_repository = (
            semester_repository
        )

    def execute(
        self,
        university_id: str,
    ):

        if not university_id:

            raise ValueError(
                "University ID không được để trống."
            )

        semesters = (
            self.semester_repository
            .get_active_planned(
                university_id=university_id,
            )
        )

        return [
            SemesterContentDTO(
                semester_id=semester.semester_id,

                name=semester.name,

                semester_number=(
                    semester.semester_number
                ),

                academic_year_id=(
                    semester.academic_year_id
                ),

                academic_year_name=(
                    semester.academic_year_name
                ),

                university_id=(
                    semester.university_id
                ),

                university_name=(
                    semester.university_name
                ),

                status=semester.status,
            )
            for semester in semesters
        ]