from apps.teachers.application.dto.teacher_dto import (
    TeacherDTO,
)


class GetUniversityTeachersUseCase:

    def __init__(
        self,
        teacher_repository,
    ):

        self.teacher_repository = teacher_repository

    def execute(
        self,
        university_id: str,
    ):

        teachers = self.teacher_repository.get_by_university(
            university_id,
        )

        return [
            TeacherDTO(
                teacher_id=teacher.teacher_id,
                full_name=teacher.full_name,
                gender=teacher.gender,
                date_of_birth=teacher.date_of_birth,
                email=teacher.email,
                phone=teacher.phone,
                department_id=teacher.department_id,
                department_name=teacher.department_name,
                university_id=teacher.university_id,
                university_name=teacher.university_name,
                status=teacher.status,
            )
            for teacher in teachers
        ]
