from apps.class_sections.application.use_cases.get_student_class_sections import (
    GetStudentClassSectionsUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_student_repository import (
    MongoClassSectionStudentRepository,
)


class_section_student_repository = (
    MongoClassSectionStudentRepository()
)

get_student_class_sections_dependency = (
    GetStudentClassSectionsUseCase(
        class_section_student_repository=(
            class_section_student_repository
        ),
    )
)