from apps.class_sections.application.use_cases.get_teacher_class_sections_use_case import (
    GetTeacherClassSectionsUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)


get_teacher_class_sections_dependency = (
    GetTeacherClassSectionsUseCase(
        class_section_repository=(
            MongoClassSectionRepository()
        ),
    )
)