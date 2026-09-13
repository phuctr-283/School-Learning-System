from apps.universities.application.dto.university_dto import (
    UniversityDTO,
)


class GetUniversitiesUseCase:

    def __init__(
        self,
        university_repository,
    ):

        self.university_repository = (
            university_repository
        )

    def execute(self):

        universities = (
            self.university_repository.get_all()
        )

        return [
            UniversityDTO(
                university_id=university.university_id,
                name=university.name,
                domain=university.domain,
                email=university.email,
                phone=university.phone,
                is_active=university.is_active,
                updated_at=university.updated_at,
            )
            for university in universities
        ]