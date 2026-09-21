from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)
from apps.class_sections.application.use_cases.get_teacher_class_sections_use_case import (
    GetTeacherClassSectionsUseCase,
)
from apps.class_sections.application.use_cases.get_teacher_active_planned_class_sections import (
    GetTeacherActivePlannedClassSectionsUseCase,
)

class_section_repository = MongoClassSectionRepository()

get_teacher_class_sections_use_case= GetTeacherClassSectionsUseCase(
    class_section_repository = class_section_repository,
)
get_teacher_active_planned_class_sections_use_case = GetTeacherActivePlannedClassSectionsUseCase(
    class_section_repository = class_section_repository,
)

