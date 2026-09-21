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
from apps.class_sections.infrastructure.persistence.models.class_section_student_model import (
    ClassSectionStudentModel,
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

    def _get_teacher_subjects_by_status(
        self,
        university_id: str,
        username: str,
        status: str | None = None,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        normalized_username = username.strip().lower()

        teacher = TeacherModel.objects(
            email=normalized_username,
        ).first()

        if not teacher:
            raise ValueError("Không tìm thấy giảng viên " "tương ứng với tài khoản.")

        department = teacher.department

        if not department:
            raise ValueError("Giảng viên chưa được gán khoa.")

        if not department.university:
            raise ValueError("Khoa của giảng viên chưa được " "gán trường đại học.")

        if department.university.university_id != university.university_id:
            raise ValueError("Giảng viên không thuộc " "trường đại học này.")

        filters = {
            "teacher": teacher,
        }

        if status is not None:
            filters["status"] = status

        class_sections = ClassSectionModel.objects(**filters).select_related()

        subjects = {}

        for class_section in class_sections:

            subject = class_section.subject

            if not subject:
                continue

            if not subject.university:
                continue

            if subject.university.university_id != university.university_id:
                continue

            if not subject.department:
                continue

            subject_id = subject.subject_id

            if subject_id in subjects:
                continue

            subjects[subject_id] = TeacherSubjectDTO(
                university_id=(university.university_id),
                department_id=(subject.department.department_id),
                subject_id=subject.subject_id,
                subject_name=subject.name,
            )

        return sorted(
            subjects.values(),
            key=lambda item: (item.subject_name.lower()),
        )

    def get_teacher_subjects(
        self,
        university_id: str,
        username: str,
    ):
        return self._get_teacher_subjects_by_status(
            university_id=university_id,
            username=username,
            status=None,
        )

    def get_teacher_active_subjects(
        self,
        university_id: str,
        username: str,
    ):
        return self._get_teacher_subjects_by_status(
            university_id=university_id,
            username=username,
            status="active",
        )

    def get_teacher_class_sections(
        self,
        university_id: str,
        username: str,
        subject_id: str,
    ):
        # =========================================
        # UNIVERSITY
        # =========================================

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        # =========================================
        # TEACHER
        # username của UserModel = email giảng viên
        # =========================================

        teacher = TeacherModel.objects(
            email=username.strip().lower(),
        ).first()

        if not teacher:
            raise ValueError("Không tìm thấy giảng viên tương ứng với tài khoản.")

        # =========================================
        # KIỂM TRA GIẢNG VIÊN THUỘC ĐÚNG TRƯỜNG
        # =========================================

        if not teacher.department:
            raise ValueError("Giảng viên chưa được gán khoa.")

        if not teacher.department.university:
            raise ValueError("Khoa của giảng viên chưa được gán trường.")

        if teacher.department.university.university_id != university.university_id:
            raise ValueError("Giảng viên không thuộc trường đại học này.")

        # =========================================
        # LẤY SUBJECT
        # =========================================

        subject = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if not subject:
            raise ValueError("Không tìm thấy môn học.")

        # =========================================
        # KIỂM TRA MÔN HỌC THUỘC CÙNG KHOA
        # =========================================

        if not subject.department:
            raise ValueError("Môn học chưa được gán khoa.")

        if subject.department.department_id != teacher.department.department_id:
            raise ValueError("Giảng viên không thuộc khoa của môn học.")

        # =========================================
        # LẤY LỚP HỌC PHẦN
        # =========================================

        class_sections = ClassSectionModel.objects(
            teacher=teacher,
            subject=subject,
            status="active",
        ).select_related()

        return [
            TeacherClassSectionDTO(
                university_id=university.university_id,
                department_id=teacher.department.department_id,
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
        # ------------------------------------------
        # Tìm năm học theo trường
        # ------------------------------------------
        academic_year = AcademicYearModel.objects(
            university=university,
            name=academic_year_name,
        ).first()

        if not academic_year:
            return None

        # ------------------------------------------
        # Tìm học kỳ thuộc năm học
        # ------------------------------------------
        semester = SemesterModel.objects(
            academic_year=academic_year,
            semester_number=str(semester_number),
        ).first()

        if not semester:
            return None

        # ------------------------------------------
        # Tìm môn học thuộc trường
        # ------------------------------------------
        subject = SubjectModel.objects(
            name=subject_name,
        ).first()

        if not subject:
            return None

        # ------------------------------------------
        # Tìm giảng viên
        # ------------------------------------------
        teacher = TeacherModel.objects(
            teacher_id=teacher_id,
        ).first()

        if not teacher:
            return None

        # ------------------------------------------
        # ClassSectionModel không có university
        # ------------------------------------------
        return ClassSectionModel.objects(
            subject=subject,
            group_number=group_number,
            semester=semester,
            academic_year=academic_year,
            teacher=teacher,
        ).first()

    
    def get_teacher_active_planned_subjects(
        self,
        university_id: str,
        username: str,
        academic_year_id: str,
        semester_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        academic_year = AcademicYearModel.objects(
            academic_year_id=academic_year_id,
            university=university,
        ).first()

        if not academic_year:
            raise ValueError("Không tìm thấy năm học.")

        semester = SemesterModel.objects(
            semester_id=semester_id,
            academic_year=academic_year,
        ).first()

        if not semester:
            raise ValueError("Không tìm thấy học kỳ.")

        normalized_username = username.strip().lower()

        teacher = TeacherModel.objects(
            email=normalized_username,
        ).first()

        if not teacher:
            raise ValueError("Không tìm thấy giảng viên tương ứng với tài khoản.")

        if not teacher.department:
            raise ValueError("Giảng viên chưa được gán khoa.")

        if not teacher.department.university:
            raise ValueError("Khoa của giảng viên chưa được gán trường.")

        if teacher.department.university.university_id != university.university_id:
            raise ValueError("Giảng viên không thuộc trường đại học này.")

        class_sections = ClassSectionModel.objects(
            teacher=teacher,
            academic_year=academic_year,
            semester=semester,
            status__in=[
                "active",
                "planned",
            ],
        ).select_related()

        subjects = {}

        for class_section in class_sections:

            subject = class_section.subject

            if not subject:
                continue

            if not subject.university:
                continue

            if subject.university.university_id != university.university_id:
                continue

            if subject.status != "active":
                continue

            if not subject.department:
                continue

            if subject.department.department_id != teacher.department.department_id:
                continue

            subject_id = subject.subject_id

            if subject_id in subjects:
                continue

            subjects[subject_id] = TeacherSubjectDTO(
                university_id=university.university_id,
                department_id=subject.department.department_id,
                subject_id=subject.subject_id,
                subject_name=subject.name,
            )

        return sorted(
            subjects.values(),
            key=lambda item: (item.subject_name.lower()),
        )

    def get_teacher_active_planned_class_sections(
        self,
        university_id: str,
        username: str,
        subject_id: str,
        academic_year_id: str,
        semester_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        academic_year = AcademicYearModel.objects(
            academic_year_id=academic_year_id,
            university=university,
        ).first()

        if not academic_year:
            raise ValueError("Không tìm thấy năm học.")

        semester = SemesterModel.objects(
            semester_id=semester_id,
            academic_year=academic_year,
        ).first()

        if not semester:
            raise ValueError("Không tìm thấy học kỳ.")

        normalized_username = username.strip().lower()

        teacher = TeacherModel.objects(
            email=normalized_username,
        ).first()

        if not teacher:
            raise ValueError("Không tìm thấy giảng viên tương ứng với tài khoản.")

        if not teacher.department:
            raise ValueError("Giảng viên chưa được gán khoa.")

        if not teacher.department.university:
            raise ValueError("Khoa của giảng viên chưa được gán trường.")

        if teacher.department.university.university_id != university.university_id:
            raise ValueError("Giảng viên không thuộc trường đại học này.")

        subject = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if not subject:
            raise ValueError("Không tìm thấy môn học.")

        if subject.status != "active":
            raise ValueError("Môn học hiện không hoạt động.")

        if not subject.department:
            raise ValueError("Môn học chưa được gán khoa.")

        if subject.department.department_id != teacher.department.department_id:
            raise ValueError("Giảng viên không thuộc khoa của môn học.")

        class_sections = ClassSectionModel.objects(
            teacher=teacher,
            subject=subject,
            academic_year=academic_year,
            semester=semester,
            status__in=[
                "active",
                "planned",
            ],
        ).select_related()

        result = []

        for class_section in class_sections:

            result.append(
                TeacherClassSectionDTO(
                    university_id=university.university_id,
                    department_id=teacher.department.department_id,
                    class_section_id=(class_section.class_section_id),
                    academic_year_id=(academic_year.academic_year_id),
                    academic_year_name=(academic_year.name),
                    semester_id=(semester.semester_id),
                    semester_name=(semester.name),
                    semester_number=(str(semester.semester_number)),
                    subject_id=(subject.subject_id),
                    subject_name=(subject.name),
                    group_number=(class_section.group_number),
                    status=(class_section.status),
                )
            )

        result.sort(key=lambda item: item.group_number)

        return result
