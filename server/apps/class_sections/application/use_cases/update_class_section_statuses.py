from apps.class_sections.domain.services.class_section_status_service import (
    ClassSectionStatusService,
)


class UpdateClassSectionStatusesUseCase:

    def __init__(
        self,
        class_section_repository,
    ):
        self.class_section_repository = class_section_repository

    def execute(
        self,
        university_id: str,
    ):

        class_sections = self.class_section_repository.get_by_university(
            university_id=university_id,
        )

        updated_class_sections = []

        for class_section in class_sections:

            new_status = ClassSectionStatusService.calculate(
                start_date=class_section.start_date,
                end_date=class_section.end_date,
            )

            if class_section.status != new_status:

                class_section = self.class_section_repository.update_status(
                    university_id=university_id,
                    class_section_id=(class_section.class_section_id),
                    status=new_status,
                )

            updated_class_sections.append(class_section)

        return updated_class_sections
