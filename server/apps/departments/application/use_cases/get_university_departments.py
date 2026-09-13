from apps.departments.application.dto.department_dto import (
    DepartmentDTO,
)


class GetUniversityDepartmentsUseCase:

    def __init__(
        self,
        department_repository,
    ):

        self.department_repository = department_repository

    def execute(
        self,
        university_id: str,
    ):

        if not university_id:

            raise ValueError("Không xác định được trường đại học")

        departments = self.department_repository.get_by_university(university_id)

        return [
            DepartmentDTO(
                department_id=department.department_id,
                department_number=(department.department_number),
                name=department.name,
                university_id=(department.university_id),
                university_name=(department.university_name),
                head_id=department.head_id,
                head_name=department.head_name,
                is_active=department.is_active,
            )
            for department in departments
        ]
