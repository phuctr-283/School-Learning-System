from apps.class_sections.infrastructure.services.excel_class_section_student_import_service import (
    ClassSectionStudentImportService,
)

from apps.class_sections.application.use_cases.import_class_section_students_by_teacher import (
    ImportClassSectionStudentsByTeacherUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)

from apps.students.infrastructure.persistence.repositories.mongo_student_repository import (
    MongoStudentRepository,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_student_repository import (
    MongoClassSectionStudentRepository,
)


class_section_repository = (
    MongoClassSectionRepository()
)

student_repository = (
    MongoStudentRepository()
)

class_section_student_repository = (
    MongoClassSectionStudentRepository()
)

import_service = (
    ClassSectionStudentImportService()
)


import_class_section_students_by_teacher_dependency = (
    ImportClassSectionStudentsByTeacherUseCase(
        class_section_repository=(
            class_section_repository
        ),

        student_repository=(
            student_repository
        ),

        class_section_student_repository=(
            class_section_student_repository
        ),

        import_service=import_service,
    )
)
