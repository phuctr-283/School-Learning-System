from apps.students.domain.entities.student_entity import (
    Student,
)

from apps.students.domain.repositories.student_repository import (
    StudentRepository,
)

from apps.students.infrastructure.persistence.models.student_model import (
    StudentModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoStudentRepository(StudentRepository):

    def get_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        students = (
            StudentModel.objects(
                university=university,
            )
            .order_by("student_id")
            .select_related()
        )

        result = []

        for student in students:

            department = student.department

            result.append(
                Student(
                    student_id=student.student_id,
                    full_name=student.full_name,
                    gender=student.gender,
                    student_class=student.student_class,
                    department_id=(department.department_id),
                    department_name=(department.name),
                    cohort_id=student.cohort_id,
                    status=student.status,
                    university_id=(university.university_id),
                    university_name=(university.name),
                    date_of_birth=(student.date_of_birth),
                    email=student.email,
                    phone=student.phone,
                )
            )

        return result

    def exists_by_student_id(
        self,
        university_id: str,
        student_id: str,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        return (
            StudentModel.objects(
                university=university,
                student_id=student_id,
            ).first()
            is not None
        )

    def exists_by_email(
        self,
        university_id: str,
        email: str,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        return (
            StudentModel.objects(
                university=university,
                email=email,
            ).first()
            is not None
        )

    def create(
        self,
        student,
        university,
        department,
    ):

        student_model = StudentModel(
            student_id=student.student_id,
            full_name=student.full_name,
            gender=student.gender,
            date_of_birth=student.date_of_birth,
            email=student.email,
            phone=student.phone,
            student_class=student.student_class,
            university=university,
            department=department,
            cohort_id=student.cohort_id,
            status=student.status,
        )

        student_model.save()

        return student_model

    def find_by_student_id(
        self,
        university_id: str,
        student_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        return StudentModel.objects(
            university=university,
            student_id=student_id,
        ).first()
