const ClassSectionRepositoryImpl = require("../../../infrastructure/repositories/class_section/class_section_repository_impl");

const GetClassSectionsUseCase = require("../../../application/class_sections/use_cases/get_class_sections");
const ImportClassSectionUseCase = require("../../../application/class_sections/use_cases/import_class_section");
const GetTeacherSubjectsUseCase = require("../../../application/class_sections/use_cases/get_teacher_subjects");
const GetTeacherActiveSubjectsUseCase = require("../../../application/class_sections/use_cases/get_teacher_active_subjects");
const GetTeacherClassSectionsUseCase = require("../../../application/class_sections/use_cases/get_teacher_class_sections");
const GetStudentClassSectionsUseCase = require("../../../application/class_sections/use_cases/get_student_class_sections");
const GetTeacherActivePlannedSubjectsUseCase = require("../../../application/class_sections/use_cases/get_teacher_active_planned_subjects");
const GetTeacherActivePlannedClassSectionsUseCase = require("../../../application/class_sections/use_cases/get_teacher_active_planned_class_sections");

const classSectionRepository = new ClassSectionRepositoryImpl();

const getClassSectionsUseCase = new GetClassSectionsUseCase(
  classSectionRepository,
);
const importClassSectionUseCase = new ImportClassSectionUseCase(
  classSectionRepository,
);
const getTeacherSubjectsUseCase = new GetTeacherSubjectsUseCase(
  new ClassSectionRepositoryImpl(),
);
const getTeacherActiveSubjectsUseCase = new GetTeacherActiveSubjectsUseCase(
  classSectionRepository,
);
const getTeacherClassSectionsUseCase = new GetTeacherClassSectionsUseCase(
  new ClassSectionRepositoryImpl(),
);
const getStudentClassSectionsUseCase = new GetStudentClassSectionsUseCase(
  classSectionRepository,
);
const getTeacherActivePlannedSubjectsUseCase =
  new GetTeacherActivePlannedSubjectsUseCase(classSectionRepository);

const getTeacherActivePlannedClassSectionsUseCase =
  new GetTeacherActivePlannedClassSectionsUseCase(classSectionRepository);
module.exports = {
  classSectionRepository,

  getClassSectionsUseCase,
  importClassSectionUseCase,
  getTeacherSubjectsUseCase,
  getTeacherActiveSubjectsUseCase,
  getTeacherClassSectionsUseCase,
  getStudentClassSectionsUseCase,
  getTeacherActivePlannedSubjectsUseCase,
  getTeacherActivePlannedClassSectionsUseCase,
};
