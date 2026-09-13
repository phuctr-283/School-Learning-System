from apps.students.application.dto.student_dto import (
    StudentDTO,
)


class GetStudentsUseCase:

    def __init__(
        self,
        student_repository,
    ):
        self.student_repository = student_repository

    def execute(
        self,
        university_id: str,
    ):

        students = self.student_repository.get_by_university(
            university_id=university_id,
        )

        return [
            StudentDTO(
                student_id=student.student_id,
                full_name=student.full_name,
                gender=student.gender,
                student_class=(student.student_class),
                department_id=(student.department_id),
                department_name=(student.department_name),
                cohort_id=student.cohort_id,
                status=student.status,
                university_id=(student.university_id),
                university_name=(student.university_name),
                date_of_birth=(student.date_of_birth),
                email=student.email,
                phone=student.phone,
            )
            for student in students
        ]
