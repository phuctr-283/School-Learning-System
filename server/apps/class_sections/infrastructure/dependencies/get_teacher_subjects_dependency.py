from apps.class_sections.application.use_cases.get_teacher_subjects_use_case import (
    GetTeacherSubjectsUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)
from apps.class_sections.application.use_cases.get_teacher_active_subjects_use_case import (
    GetTeacherActiveSubjectsUseCase,
)
from apps.class_sections.application.use_cases.get_teacher_active_planned_subjects import (
    GetTeacherActivePlannedSubjectsUseCase
)

class_section_repository = MongoClassSectionRepository()

get_teacher_subjects_use_case = GetTeacherSubjectsUseCase(
    class_section_repository=(class_section_repository),
)
get_teacher_active_subjects_use_case = GetTeacherActiveSubjectsUseCase(
    class_section_repository=class_section_repository,
)
get_teacher_active_planned_subjects_use_case = GetTeacherActivePlannedSubjectsUseCase(
    class_section_repository = class_section_repository
)
