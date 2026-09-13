from apps.departments.application.dto.department_dto import (
    DepartmentDTO,
)


class GetActiveDepartmentsUseCase:

    def __init__(
        self,
        department_repository,
    ):
        self.department_repository = (
            department_repository
        )

    def execute(
        self,
        university_id: str,
    ):
        departments = (
            self.department_repository
            .get_active_by_university_authenticated(
                university_id=university_id,
            )
        )

        return [
            DepartmentDTO(
                department_id=department.department_id,
                department_number=department.department_number,
                name=department.name,

                university_id=department.university_id,
                university_name=department.university_name,

                head_id=department.head_id,
                head_name=department.head_name,

                is_active=department.is_active,
            )
            for department in departments
        ]