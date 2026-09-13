from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)

from apps.subjects.infrastructure.persistence.repositories.mongo_subject_repository import (
    MongoSubjectRepository,
)

from apps.teachers.infrastructure.persistence.repositories.mongo_teacher_repository import (
    MongoTeacherRepository,
)

from apps.semesters.infrastructure.persistence.repositories.mongo_semester_repository import (
    MongoSemesterRepository,
)

from apps.academic_years.infrastructure.persistence.repositories.mongo_academic_year_repository import (
    MongoAcademicYearRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.class_sections.application.use_cases.get_class_sections import (
    GetClassSectionsUseCase,
)

from apps.class_sections.application.use_cases.update_class_section_statuses import (
    UpdateClassSectionStatusesUseCase,
)

from apps.class_sections.application.use_cases.import_class_sections import (
    ImportClassSectionsUseCase,
)

from apps.class_sections.infrastructure.services.excel_class_section_import_service import (
    ExcelClassSectionImportService,
)

from apps.lessons.infrastructure.dependencies.lesson_dependency import (
    ensure_lesson_plans_dependency
)

class_section_repository = MongoClassSectionRepository()

subject_repository = MongoSubjectRepository()

teacher_repository = MongoTeacherRepository()

semester_repository = MongoSemesterRepository()

academic_year_repository = MongoAcademicYearRepository()

university_repository = MongoUniversityRepository()

excel_class_section_import_service = ExcelClassSectionImportService()


update_class_section_statuses_use_case = UpdateClassSectionStatusesUseCase(
    class_section_repository=class_section_repository,
)

get_class_sections_use_case = GetClassSectionsUseCase(
    class_section_repository,
    update_class_section_statuses_use_case,
)


import_class_sections_use_case = ImportClassSectionsUseCase(
    class_section_repository=class_section_repository,
    subject_repository=subject_repository,
    teacher_repository=teacher_repository,
    semester_repository=semester_repository,
    academic_year_repository=academic_year_repository,
    university_repository=university_repository,
    update_class_section_statuses_use_case=(update_class_section_statuses_use_case),
    ensure_lesson_plans_use_case=(
        ensure_lesson_plans_dependency
    ),
)
