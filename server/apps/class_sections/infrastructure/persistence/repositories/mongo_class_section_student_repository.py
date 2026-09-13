from datetime import datetime
from typing import List

from apps.students.domain.entities.student_entity import Student

from apps.class_sections.domain.repositories.class_section_student_repository import (
    ClassSectionStudentRepository,
)

from apps.class_sections.infrastructure.persistence.models.class_section_student_model import (
    ClassSectionStudentModel,
)


class MongoClassSectionStudentRepository(
    ClassSectionStudentRepository,
):

    def _to_student_entity(
        self,
        enrollment,
    ) -> Student:

        student = enrollment.student

        return Student(
            student_id=student.student_id,

            full_name=student.full_name,

            gender=student.gender,

            student_class=student.student_class,

            department_id=(
                student.department.department_id
                if student.department
                else None
            ),

            department_name=(
                student.department.name
                if student.department
                else None
            ),

            cohort_id=(
                student.cohort.cohort_id
                if student.cohort
                else None
            ),

            cohort_name=(
                student.cohort.name
                if student.cohort
                else None
            ),

            email=student.email,

            phone=student.phone,

            date_of_birth=student.date_of_birth,

            status=student.status,
        )

    def exists(
        self,
        class_section,
        student,
    ) -> bool:

        return (
            ClassSectionStudentModel.objects(
                class_section=class_section,
                student=student,
            )
            .first()
            is not None
        )

    def add(
        self,
        class_section,
        student,
    ):

        exists = (
            ClassSectionStudentModel.objects(
                class_section=class_section,
                student=student,
            )
            .first()
        )

        if exists:
            return exists

        enrollment = (
            ClassSectionStudentModel(
                class_section=class_section,
                student=student,
                created_at=datetime.utcnow(),
            )
        )

        enrollment.save()

        return enrollment

    def get_students_by_class_section(
        self,
        class_section,
    ) -> List[Student]:

        enrollments = list(
            ClassSectionStudentModel.objects(
                class_section=class_section,
            )
            .select_related()
        )

        students = [
            self._to_student_entity(
                enrollment
            )
            for enrollment in enrollments
        ]

        students.sort(
            key=lambda student: (
                (
                    student.student_class
                    or ""
                )
                .strip()
                .upper(),

                (
                    student.student_id
                    or ""
                )
                .strip()
                .upper(),
            )
        )

        return students