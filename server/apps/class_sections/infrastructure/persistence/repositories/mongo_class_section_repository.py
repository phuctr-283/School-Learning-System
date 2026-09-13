from apps.class_sections.domain.repositories.class_section_repository import (
    ClassSectionRepository,
)

from apps.class_sections.domain.entities.class_section_entity import (
    ClassSection,
)

from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)
from apps.subjects.infrastructure.persistence.models.subject_model import (
    SubjectModel,
)
from apps.academic_years.infrastructure.persistence.models.academic_year_model import (
    AcademicYearModel,
)
from apps.semesters.infrastructure.persistence.models.semester_model import (
    SemesterModel,
)
from apps.teachers.infrastructure.persistence.models.teacher_model import TeacherModel
from apps.class_sections.application.dto.teacher_subject_dto import TeacherSubjectDTO
from apps.class_sections.application.dto.teacher_class_section_dto import (
    TeacherClassSectionDTO,
)
from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)


class MongoClassSectionRepository(ClassSectionRepository):

    def get_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(university_id=university_id).first()

        if not university:
            return []

        subjects = SubjectModel.objects(
            university=university,
        )

        class_sections = ClassSectionModel.objects(
            subject__in=subjects,
        )

        result = []

        for class_section in class_sections:

            subject = class_section.subject
            teacher = class_section.teacher
            semester = class_section.semester
            academic_year = class_section.academic_year

            result.append(
                ClassSection(
                    class_section_id=class_section.class_section_id,
                    subject_id=subject.subject_id,
                    subject_name=subject.name,
                    group_number=class_section.group_number,
                    teacher_id=teacher.teacher_id,
                    teacher_name=teacher.full_name,
                    semester_id=semester.semester_id,
                    semester_name=semester.name,
                    semester_number=semester.semester_number,
                    academic_year_id=academic_year.academic_year_id,
                    academic_year_name=academic_year.name,
                    university_id=university.university_id,
                    university_name=university.name,
                    start_date=class_section.start_date,
                    end_date=class_section.end_date,
                    status=class_section.status,
                )
            )

        return result

    def exists_by_group(
        self,
        university_id: str,
        subject_id: str,
        group_number: int,
        semester_id: str,
        academic_year_id: str,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        # =========================================
        # SUBJECT
        # =========================================

        subject = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if not subject:
            return False

        # =========================================
        # ACADEMIC YEAR
        # =========================================

        academic_year = AcademicYearModel.objects(
            academic_year_id=academic_year_id,
            university=university,
        ).first()

        if not academic_year:
            return False

        # =========================================
        # SEMESTER
        # =========================================

        semester = SemesterModel.objects(
            semester_id=semester_id,
            academic_year=academic_year,
        ).first()

        if not semester:
            return False

        # =========================================
        # CLASS SECTION
        # =========================================

        exists = ClassSectionModel.objects(
            subject=subject,
            group_number=group_number,
            semester=semester,
            academic_year=academic_year,
        ).first()

        return exists is not None

    def create(
        self,
        class_section,
        university_id: str,
        subject_id: str,
        teacher_id: str,
        semester_id: str,
        academic_year_id: str,
    ):

        # =========================================
        # UNIVERSITY
        # =========================================

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError(f"Không tìm thấy trường đại học '{university_id}'.")

        # =========================================
        # SUBJECT
        # =========================================

        subject = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if not subject:
            raise ValueError(f"Không tìm thấy môn học '{subject_id}'.")

        # =========================================
        # TEACHER
        # =========================================

        teacher = TeacherModel.objects(
            teacher_id=teacher_id,
        ).first()

        if not teacher:
            raise ValueError(f"Không tìm thấy giảng viên '{teacher_id}'.")

        # =========================================
        # ACADEMIC YEAR
        # =========================================

        academic_year = AcademicYearModel.objects(
            academic_year_id=academic_year_id,
            university=university,
        ).first()

        if not academic_year:
            raise ValueError(f"Không tìm thấy năm học '{academic_year_id}'.")

        # =========================================
        # SEMESTER
        # =========================================

        semester = SemesterModel.objects(
            semester_id=semester_id,
            academic_year=academic_year,
        ).first()

        if not semester:
            raise ValueError(f"Không tìm thấy học kỳ '{semester_id}'.")

        # =========================================
        # CREATE
        # =========================================

        model = ClassSectionModel(
            class_section_id=class_section.class_section_id,
            subject=subject,
            group_number=class_section.group_number,
            teacher=teacher,
            semester=semester,
            academic_year=academic_year,
            start_date=class_section.start_date,
            end_date=class_section.end_date,
            status=class_section.status,
        )

        model.save()

        # =========================================
        # RETURN DOMAIN ENTITY
        # =========================================

        return ClassSection(
            class_section_id=model.class_section_id,
            subject_id=subject.subject_id,
            subject_name=subject.name,
            group_number=model.group_number,
            teacher_id=teacher.teacher_id,
            teacher_name=teacher.full_name,
            semester_id=semester.semester_id,
            semester_name=semester.name,
            semester_number=semester.semester_number,
            academic_year_id=academic_year.academic_year_id,
            academic_year_name=academic_year.name,
            university_id=university.university_id,
            university_name=university.name,
            start_date=model.start_date,
            end_date=model.end_date,
            status=model.status,
        )

    def update_status(
        self,
        university_id: str,
        class_section_id: str,
        status: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        subjects = SubjectModel.objects(
            university=university,
        )

        class_section = ClassSectionModel.objects(
            class_section_id=class_section_id,
            subject__in=subjects,
        ).first()

        if not class_section:
            return None

        class_section.status = status

        class_section.save(
            validate=False,
        )

        subject = class_section.subject
        teacher = class_section.teacher
        semester = class_section.semester
        academic_year = class_section.academic_year

        return ClassSection(
            class_section_id=class_section.class_section_id,
            subject_id=subject.subject_id,
            subject_name=subject.name,
            group_number=class_section.group_number,
            teacher_id=teacher.teacher_id,
            teacher_name=teacher.full_name,
            semester_id=semester.semester_id,
            semester_name=semester.name,
            semester_number=semester.semester_number,
            academic_year_id=academic_year.academic_year_id,
            academic_year_name=academic_year.name,
            university_id=university.university_id,
            university_name=university.name,
            start_date=class_section.start_date,
            end_date=class_section.end_date,
            status=class_section.status,
        )

    def get_teacher_subjects(
        self,
        university_id: str,
        department_id: str,
        teacher_id: str,
    ):
        university = UniversityModel.objects(university_id=university_id).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        department = DepartmentModel.objects(
            department_id=department_id,
            university=university,
        ).first()

        if not department:
            raise ValueError("Không tìm thấy khoa.")

        teacher = TeacherModel.objects(
            teacher_id=teacher_id,
            department=department,
        ).first()

        if not teacher:
            raise ValueError("Không tìm thấy giảng viên.")

        class_sections = ClassSectionModel.objects(
            teacher=teacher,
            status="active",
        ).select_related()

        subjects = {}

        for class_section in class_sections:

            subject = class_section.subject

            if not subject:
                continue

            if (
                not subject.university
                or subject.university.university_id != university.university_id
            ):
                continue

            subjects[subject.subject_id] = TeacherSubjectDTO(
                university_id=(university.university_id),
                department_id=(department.department_id),
                subject_id=(subject.subject_id),
                subject_name=subject.name,
            )

        return list(subjects.values())

    def get_teacher_class_sections(
        self,
        university_id: str,
        department_id: str,
        teacher_id: str,
        subject_id: str,
    ):
        university = UniversityModel.objects(university_id=university_id).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        department = DepartmentModel.objects(
            department_id=department_id,
            university=university,
        ).first()

        if not department:
            raise ValueError("Không tìm thấy khoa.")

        teacher = TeacherModel.objects(
            teacher_id=teacher_id,
            department=department,
        ).first()

        if not teacher:
            raise ValueError("Không tìm thấy giảng viên.")

        subject = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if not subject:
            raise ValueError("Không tìm thấy môn học.")

        class_sections = ClassSectionModel.objects(
            teacher=teacher,
            subject=subject,
            status="active",
        ).select_related()

        return [
            TeacherClassSectionDTO(
                class_section_id=class_section.class_section_id,
                academic_year_id=(class_section.academic_year.academic_year_id),
                academic_year_name=(class_section.academic_year.name),
                semester_id=(class_section.semester.semester_id),
                semester_name=(class_section.semester.name),
                semester_number=(class_section.semester.semester_number),
                subject_id=(class_section.subject.subject_id),
                subject_name=(class_section.subject.name),
                group_number=class_section.group_number,
                status=class_section.status,
            )
            for class_section in class_sections
        ]

    def find_by_import_info_and_teacher(
        self,
        university_id: str,
        subject_name: str,
        group_number: int,
        semester_number: int,
        academic_year_name: str,
        teacher_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        teacher = TeacherModel.objects(
            teacher_id=teacher_id,
        ).first()

        if not teacher:
            return None

        if not teacher.department or teacher.department.university != university:
            return None

        academic_year = AcademicYearModel.objects(
            university=university,
            name=academic_year_name,
        ).first()

        if not academic_year:
            return None

        semester = SemesterModel.objects(
            academic_year=academic_year,
            semester_number=str(semester_number),
        ).first()

        if not semester:
            return None

        subject = SubjectModel.objects(
            university=university,
            name=subject_name,
        ).first()

        if not subject:
            return None

        return ClassSectionModel.objects(
            university=university,
            teacher=teacher,
            academic_year=academic_year,
            semester=semester,
            subject=subject,
            group_number=group_number,
            status="active",
        ).first()
