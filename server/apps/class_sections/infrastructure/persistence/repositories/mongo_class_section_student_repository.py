from datetime import datetime
from typing import List

from apps.students.domain.entities.student_entity import Student

from apps.class_sections.domain.repositories.class_section_student_repository import (
    ClassSectionStudentRepository,
)

from apps.class_sections.infrastructure.persistence.models.class_section_student_model import (
    ClassSectionStudentModel,
)
from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)
from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)
from apps.students.infrastructure.persistence.models.student_model import (
    StudentModel,
)
from apps.subjects.infrastructure.persistence.models.subject_model import (
    SubjectModel,
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
                student.department.department_id if student.department else None
            ),
            department_name=(student.department.name if student.department else None),
            cohort_id=(student.cohort.cohort_id if student.cohort else None),
            cohort_name=(student.cohort.name if student.cohort else None),
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
            ).first()
            is not None
        )

    def add(
        self,
        class_section,
        student,
    ):

        exists = ClassSectionStudentModel.objects(
            class_section=class_section,
            student=student,
        ).first()

        if exists:
            return exists

        enrollment = ClassSectionStudentModel(
            class_section=class_section,
            student=student,
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
            ).select_related()
        )

        students = [self._to_student_entity(enrollment) for enrollment in enrollments]

        students.sort(
            key=lambda student: (
                (student.student_class or "").strip().upper(),
                (student.student_id or "").strip().upper(),
            )
        )

        return students

    def get_student_class_sections(
    self,
    student_id: str,
    university_id: str,
):
        print(
            "STUDENT CLASS SECTIONS:",
            student_id,
            university_id,
        )

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        print(
            "UNIVERSITY:",
            university,
        )

        if not university:
            print("UNIVERSITY NOT FOUND")
            return []

        student = StudentModel.objects(
    student_id=student_id,
).first()

        print(
            "STUDENT:",
            student,
        )

        if not student:
            print("STUDENT NOT FOUND")
            return []
        if student.department is None:
            print("STUDENT DEPARTMENT NOT FOUND")
            return []

        if student.department.university != university:
            print("STUDENT UNIVERSITY NOT FOUND")
            return []
        subjects = list(
            SubjectModel.objects(
                university=university,
            )
        )

        print(
            "SUBJECT COUNT:",
            len(subjects),
        )

        if not subjects:
            print("SUBJECTS NOT FOUND")
            return []

        class_sections = list(
            ClassSectionModel.objects(
                subject__in=subjects,
                status="active",
            ).select_related()
        )

        print(
            "CLASS SECTION COUNT:",
            len(class_sections),
        )

        for class_section in class_sections:
            print(
                "CLASS SECTION:",
                class_section.class_section_id,
                class_section.status,
                class_section.subject.subject_id,
            )

        if not class_sections:
            print("ACTIVE CLASS SECTIONS NOT FOUND")
            return []

        enrollments = list(
            ClassSectionStudentModel.objects(
                student=student,
                class_section__in=class_sections,
            ).select_related()
        )

        print(
            "ENROLLMENT COUNT:",
            len(enrollments),
        )

        for enrollment in enrollments:
            print(
                "ENROLLMENT:",
                enrollment.student.student_id,
                enrollment.class_section.class_section_id,
            )

        result = []

        for enrollment in enrollments:
            class_section = enrollment.class_section

            if not class_section:
                continue

            subject = class_section.subject

            if not subject:
                continue

            teacher = class_section.teacher
            semester = class_section.semester
            academic_year = class_section.academic_year

            if not semester or not academic_year:
                continue

            result.append(
                {
                    "class_section_id": str(
                        class_section.class_section_id
                    ),
                    "academic_year_id": str(
                        academic_year.academic_year_id
                    ),
                    "semester_id": str(
                        semester.semester_id
                    ),
                    "subject_id": str(
                        subject.subject_id
                    ),
                    "group_number": class_section.group_number,
                    "subject_name": subject.name,
                    "teacher_name": (
                        teacher.full_name
                        if teacher
                        else "Chưa phân công"
                    ),
                }
            )

        print(
            "RESULT COUNT:",
            len(result),
        )

        return result