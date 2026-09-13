const ClassSectionRepositoryImpl = require("../../../infrastructure/repositories/class_section/class_section_repository_impl");

const GetClassSectionsUseCase = require("../../../application/class_sections/use_cases/get_class_sections");
const ImportClassSectionUseCase = require("../../../application/class_sections/use_cases/import_class_section");
const GetTeacherSubjectsUseCase = require("../../../application/class_sections/use_cases/get_teacher_subjects");
const GetTeacherClassSectionsUseCase = require("../../../application/class_sections/use_cases/get_teacher_class_sections");

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
const getTeacherClassSectionsUseCase = new GetTeacherClassSectionsUseCase(
  new ClassSectionRepositoryImpl(),
);
module.exports = {
  classSectionRepository,

  getClassSectionsUseCase,
  importClassSectionUseCase,
  getTeacherSubjectsUseCase,
  getTeacherClassSectionsUseCase,
};
