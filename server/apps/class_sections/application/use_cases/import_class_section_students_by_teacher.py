class ImportClassSectionStudentsByTeacherUseCase:

    def __init__(
        self,
        class_section_repository,
        student_repository,
        class_section_student_repository,
        import_service,
    ):
        self.class_section_repository = class_section_repository
        self.student_repository = student_repository
        self.class_section_student_repository = class_section_student_repository
        self.import_service = import_service

    def execute(
        self,
        file,
        teacher_id: str,
        university_id: str,
    ):
        import_data = self.import_service.read(file)

        # ==========================================
        # Chuẩn hóa dữ liệu từ file Excel
        # ==========================================
        subject_name = str(import_data["subject_name"] or "").strip()

        academic_year_name = str(import_data["academic_year_name"] or "").strip()

        teacher_id = str(teacher_id or "").strip()

        university_id = str(university_id or "").strip()

        group_number = self._parse_integer(
            import_data["group_number"],
            "Số nhóm",
        )

        semester_number = self._parse_integer(
            import_data["semester_number"],
            "Số học kỳ",
        )

        if not subject_name:
            raise ValueError("Tên môn học trong file Excel không được để trống")

        if not academic_year_name:
            raise ValueError("Tên năm học trong file Excel không được để trống")

        students = import_data["students"]

        # ==========================================
        # Tìm lớp học phần của giảng viên
        # ==========================================
        class_section = self.class_section_repository.find_by_import_info_and_teacher(
            university_id=university_id,
            subject_name=subject_name,
            group_number=group_number,
            semester_number=semester_number,
            academic_year_name=academic_year_name,
            teacher_id=teacher_id,
        )

        if not class_section:
            raise ValueError(
                f"Bạn không phải giảng viên của môn "
                f"'{subject_name}', "
                f"nhóm {group_number}, "
                f"học kỳ {semester_number}, "
                f"năm học '{academic_year_name}'"
            )

        imported = []
        skipped = []
        not_found = []

        for student_row in students:

            student_id = str(student_row.student_id or "").strip()

            full_name = str(student_row.full_name or "").strip()

            student_class = str(student_row.student_class or "").strip()

            if not student_id:
                continue

            student = self.student_repository.find_by_student_id(
                university_id=university_id,
                student_id=student_id,
            )

            if not student:
                not_found.append(
                    {
                        "student_id": student_id,
                        "full_name": full_name,
                        "student_class": student_class,
                    }
                )

                continue

            exists = self.class_section_student_repository.exists(
                class_section=class_section,
                student=student,
            )

            if exists:
                skipped.append(student_id)
                continue

            self.class_section_student_repository.add(
                class_section=class_section,
                student=student,
            )

            imported.append(student_id)

        return {
            "message": (
                f"Đã thêm {len(imported)} sinh viên mới, "
                f"bỏ qua {len(skipped)} sinh viên đã có"
            ),
            "subject_name": subject_name,
            "group_number": group_number,
            "semester_number": semester_number,
            "academic_year_name": academic_year_name,
            "imported_count": len(imported),
            "skipped_count": len(skipped),
            "not_found_count": len(not_found),
            "imported": imported,
            "skipped": skipped,
            "not_found": not_found,
        }

    @staticmethod
    def _parse_integer(value, field_name: str) -> int:
        try:
            return int(str(value).strip())

        except (TypeError, ValueError):
            raise ValueError(f"{field_name} trong file Excel phải là số nguyên")
