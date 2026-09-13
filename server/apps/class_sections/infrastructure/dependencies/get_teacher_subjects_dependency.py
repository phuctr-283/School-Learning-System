from apps.class_sections.application.use_cases.get_teacher_subjects_use_case import (
    GetTeacherSubjectsUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)


get_teacher_subjects_dependency = (
    GetTeacherSubjectsUseCase(
        class_section_repository=(
            MongoClassSectionRepository()
        ),
    )
)