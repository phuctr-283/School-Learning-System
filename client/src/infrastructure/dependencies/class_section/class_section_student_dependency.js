const ClassSectionStudentRepositoryImpl = require("../../../infrastructure/repositories/class_section/class_section_student_repository_impl");

const ImportClassSectionStudentsUseCase = require("../../../application/class_sections/use_cases/import_class_section_students");

const repository = new ClassSectionStudentRepositoryImpl();

const importClassSectionStudentsUseCase = new ImportClassSectionStudentsUseCase(
  repository,
);

module.exports = {
  importClassSectionStudentsUseCase,
};
