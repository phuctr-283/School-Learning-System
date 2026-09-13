from apps.class_sections.application.dto.class_section_dto import (
    ClassSectionDTO,
)


class GetClassSectionsUseCase:

    def __init__(
        self,
        class_section_repository,
        update_class_section_statuses_use_case,
    ):
        self.class_section_repository = class_section_repository

        self.update_class_section_statuses_use_case = (
            update_class_section_statuses_use_case
        )

    def execute(
        self,
        university_id: str,
    ):

        # =====================================================
        # UPDATE STATUS TRƯỚC KHI LẤY DỮ LIỆU HIỂN THỊ
        # =====================================================

        class_sections = (
            self.update_class_section_statuses_use_case.execute(
                university_id=university_id,
            )
        )

        # =====================================================
        # CONVERT ENTITY -> DTO
        # =====================================================

        return [
            ClassSectionDTO(
                class_section_id=class_section.class_section_id,

                subject_id=class_section.subject_id,
                subject_name=class_section.subject_name,

                group_number=class_section.group_number,

                teacher_id=class_section.teacher_id,
                teacher_name=class_section.teacher_name,

                semester_id=class_section.semester_id,
                semester_name=class_section.semester_name,
                semester_number=class_section.semester_number,

                academic_year_id=class_section.academic_year_id,
                academic_year_name=class_section.academic_year_name,

                university_id=class_section.university_id,
                university_name=class_section.university_name,

                start_date=class_section.start_date,
                end_date=class_section.end_date,

                status=class_section.status,
            )
            for class_section in class_sections
        ]