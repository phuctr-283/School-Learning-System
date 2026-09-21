from apps.class_sections.domain.entities.class_section_entity import (
    ClassSection,
)

from apps.class_sections.application.dto.validated_class_section import (
    ValidatedClassSection,
)

from apps.class_sections.application.use_cases.update_class_section_statuses import (
    UpdateClassSectionStatusesUseCase,
)

from apps.class_sections.domain.services.class_section_status_service import (
    ClassSectionStatusService,
)


class ImportClassSectionsUseCase:

    def __init__(
        self,
        class_section_repository,
        subject_repository,
        teacher_repository,
        semester_repository,
        academic_year_repository,
        university_repository,
        update_class_section_statuses_use_case,
        ensure_lesson_plans_use_case,
    ):

        self.class_section_repository = class_section_repository

        self.subject_repository = subject_repository

        self.teacher_repository = teacher_repository

        self.semester_repository = semester_repository

        self.academic_year_repository = academic_year_repository

        self.university_repository = university_repository

        self.update_class_section_statuses_use_case = (
            update_class_section_statuses_use_case
        )

        self.ensure_lesson_plans_use_case = ensure_lesson_plans_use_case

    def execute(
        self,
        rows,
        university_id: str,
    ):

        # =====================================================
        # UNIVERSITY
        # =====================================================

        university = self.university_repository.find_by_id(
            university_id,
        )

        if not university:
            raise ValueError("Không tìm thấy trường.")

        # =====================================================
        # PHASE 1
        #
        # VALIDATE TOÀN BỘ FILE
        # =====================================================

        validated_items = []

        errors = []

        file_duplicates = set()

        for row_number, row in enumerate(
            rows,
            start=2,
        ):

            try:

                item = self._validate_row(
                    row=row,
                    row_number=row_number,
                    university_id=university_id,
                    university=university,
                    file_duplicates=file_duplicates,
                )

                validated_items.append(item)

            except ValueError as error:

                errors.append(f"Dòng {row_number}: {str(error)}")

        # =====================================================
        # CÓ LỖI → KHÔNG CREATE GÌ
        # =====================================================

        if errors:
            raise ValueError("\n".join(errors))

        # =====================================================
        # PHASE 2
        #
        # CREATE CLASS SECTIONS MỚI
        #
        # CLASS SECTION ĐÃ TỒN TẠI → BỎ QUA
        # =====================================================

        created_count = 0

        created_items = []

        skipped_count = 0

        skipped_items = []

        for item in validated_items:

            if item.is_existing:

                skipped_count += 1

                skipped_items.append(
                    {
                        "row_number": item.row_number,
                        "subject_name": item.subject.name,
                        "group_number": item.group_number,
                        "semester_name": item.semester.name,
                        "academic_year_name": (item.academic_year.name),
                    }
                )

                continue

            class_section = self._create_class_section(
                item=item,
                university=university,
            )

            created_items.append(class_section)

            created_count += 1

        # =====================================================
        # UPDATE STATUS
        #
        # Bao gồm cả dữ liệu cũ và dữ liệu mới
        # =====================================================

        self.update_class_section_statuses_use_case.execute(
            university_id=university_id,
        )

        # =====================================================
        # ENSURE LESSON PLANS
        #
        # Bao phủ cả 3 trường hợp:
        #
        # 1. ClassSection cũ chưa có plan
        #    → tạo plan
        #
        # 2. ClassSection mới
        #    → tạo plan
        #
        # 3. ClassSection đã có plan
        #    → repository ensure sẽ bỏ qua
        # =====================================================

        self.ensure_lesson_plans_use_case.execute(
            university_id=university_id,
        )

        return {
            "created_count": created_count,
            "skipped_count": skipped_count,
            "created_items": created_items,
            "skipped_items": skipped_items,
        }

    # =========================================================
    # PHASE 1 - VALIDATE ROW
    # =========================================================

    def _validate_row(
        self,
        row,
        row_number: int,
        university_id: str,
        university,
        file_duplicates,
    ):

        # =====================================================
        # GET VALUES
        # =====================================================

        subject_name = str(row["Tên môn"]).strip()

        group_number = int(row["Nhóm"])

        teacher_name = str(row["Tên giảng viên"]).strip()

        semester_name = str(row["Học kỳ"]).strip()

        academic_year_name = str(row["Năm học"]).strip()

        start_date = row["Ngày bắt đầu"]

        end_date = row["Ngày kết thúc"]

        # =====================================================
        # BASIC VALIDATION
        # =====================================================

        if not subject_name:
            raise ValueError("Tên môn không được để trống.")

        if group_number < 1:
            raise ValueError("Nhóm phải lớn hơn hoặc bằng 1.")

        if not teacher_name:
            raise ValueError("Tên giảng viên không được để trống.")

        if not semester_name:
            raise ValueError("Học kỳ không được để trống.")

        if not academic_year_name:
            raise ValueError("Năm học không được để trống.")

        # =====================================================
        # VALIDATE DATE
        # =====================================================

        if not start_date:
            raise ValueError("Ngày bắt đầu không được để trống.")

        if not end_date:
            raise ValueError("Ngày kết thúc không được để trống.")

        if start_date > end_date:
            raise ValueError("Ngày bắt đầu phải trước " "hoặc bằng ngày kết thúc.")

        # =====================================================
        # ACADEMIC YEAR
        # =====================================================

        academic_year = self.academic_year_repository.get_by_name(
            university_id=university_id,
            name=academic_year_name,
        )

        if not academic_year:

            raise ValueError(f"Không tìm thấy năm học " f"'{academic_year_name}'.")

        # =====================================================
        # SEMESTER
        # =====================================================

        semester = self.semester_repository.get_by_name(
            university_id=university_id,
            academic_year_id=(academic_year.academic_year_id),
            name=semester_name,
        )

        if not semester:

            raise ValueError(
                f"Không tìm thấy "
                f"'{semester_name}' "
                f"trong năm học "
                f"'{academic_year_name}'."
            )

        # =====================================================
        # SUBJECT
        # =====================================================

        subject = self.subject_repository.get_by_name(
            name=subject_name,
            university_id=university_id,
        )

        if not subject:

            raise ValueError(f"Không tìm thấy môn học " f"'{subject_name}'.")

        # =====================================================
        # DEPARTMENT
        # =====================================================

        department = subject.department

        if department is None:
            raise ValueError(
                f"Môn học '{subject_name}' chưa được liên kết với khoa."
            )

        department_id = department.department_id

        # =====================================================
        # TEACHER
        # =====================================================

        teacher = self.teacher_repository.get_by_name(
            name=teacher_name,
            department_id=department_id,
            university_id=university_id,
        )

        if not teacher:

            raise ValueError(
                f"Không tìm thấy giảng viên "
                f"'{teacher_name}' "
                f"thuộc khoa của môn học "
                f"'{subject_name}'."
            )

        # =====================================================
        # SUBJECT + TEACHER SAME DEPARTMENT
        # =====================================================
        department_subject = subject.department
        department_id_subject = department_subject.department_id
        if department_id_subject != teacher.department_id:

            raise ValueError(
                f"Giảng viên '{teacher_name}' "
                f"không thuộc cùng khoa với "
                f"môn học '{subject_name}'."
            )

        # =====================================================
        # DATE MUST BE INSIDE SEMESTER
        # =====================================================

        if start_date < semester.start_date:

            raise ValueError(
                f"Ngày bắt đầu phải nằm trong " f"thời gian của {semester.name}."
            )

        if end_date > semester.end_date:

            raise ValueError(
                f"Ngày kết thúc phải nằm trong " f"thời gian của {semester.name}."
            )

        # =====================================================
        # DUPLICATE IN EXCEL FILE
        #
        # subject + group + semester + academic year
        # =====================================================

        duplicate_key = (
            subject.subject_id,
            group_number,
            semester.semester_id,
            academic_year.academic_year_id,
        )

        if duplicate_key in file_duplicates:

            raise ValueError(
                f"Trùng nhóm {group_number} của " f"môn '{subject_name}' trong file."
            )

        file_duplicates.add(duplicate_key)

        # =====================================================
        # CHECK DATABASE
        # =====================================================

        exists = self.class_section_repository.exists_by_group(
            university_id=university_id,
            subject_id=subject.subject_id,
            group_number=group_number,
            semester_id=semester.semester_id,
            academic_year_id=(academic_year.academic_year_id),
        )

        # =====================================================
        # VALIDATED RESULT
        #
        # exists = True
        # → Không báo lỗi
        # → Đánh dấu existing
        #
        # exists = False
        # → ClassSection mới
        # =====================================================

        return ValidatedClassSection(
            row_number=row_number,
            subject=subject,
            teacher=teacher,
            semester=semester,
            academic_year=academic_year,
            group_number=group_number,
            start_date=start_date,
            end_date=end_date,
            is_existing=exists,
        )

    # =========================================================
    # PHASE 2 - CREATE
    # =========================================================

    def _create_class_section(
        self,
        item,
        university,
    ):

        subject = item.subject

        teacher = item.teacher

        semester = item.semester

        academic_year = item.academic_year

        class_section_id = (
            f"{subject.subject_id}" f"-{semester.semester_id}" f"-{item.group_number}"
        )

        status = ClassSectionStatusService.calculate(
            start_date=item.start_date,
            end_date=item.end_date,
        )

        class_section = ClassSection(
            class_section_id=class_section_id,
            subject_id=subject.subject_id,
            subject_name=subject.name,
            group_number=item.group_number,
            teacher_id=teacher.teacher_id,
            teacher_name=teacher.full_name,
            semester_id=semester.semester_id,
            semester_name=semester.name,
            semester_number=semester.semester_number,
            academic_year_id=(academic_year.academic_year_id),
            academic_year_name=(academic_year.name),
            university_id=(university.university_id),
            university_name=(university.name),
            start_date=item.start_date,
            end_date=item.end_date,
            status=status,
        )

        return self.class_section_repository.create(
            class_section=class_section,
            university_id=university.university_id,
            subject_id=subject.subject_id,
            teacher_id=teacher.teacher_id,
            semester_id=semester.semester_id,
            academic_year_id=academic_year.academic_year_id,
        )
