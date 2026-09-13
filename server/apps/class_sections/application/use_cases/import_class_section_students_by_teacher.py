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

        subject_name = import_data["subject_name"]

        group_number = import_data["group_number"]

        semester_number = import_data["semester_number"]

        academic_year_name = import_data["academic_year_name"]

        students = import_data["students"]

        class_section = self.class_section_repository.find_by_import_info_and_teacher(
            university_id=university_id,
            subject_name=subject_name,
            group_number=group_number,
            semester_number=semester_number,
            academic_year_name=(academic_year_name),
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

            student_id = student_row.student_id

            student = self.student_repository.find_by_student_id(
                university_id=university_id,
                student_id=student_id,
            )

            if not student:

                not_found.append(
                    {
                        "student_id": student_id,
                        "full_name": (student_row.full_name),
                        "student_class": (student_row.student_class),
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
                f"Đã thêm "
                f"{len(imported)} sinh viên mới, "
                f"bỏ qua "
                f"{len(skipped)} sinh viên đã có"
            ),
            "subject_name": subject_name,
            "group_number": group_number,
            "semester_number": semester_number,
            "academic_year_name": (academic_year_name),
            "imported_count": len(imported),
            "skipped_count": len(skipped),
            "not_found_count": len(not_found),
            "imported": imported,
            "skipped": skipped,
            "not_found": not_found,
        }
