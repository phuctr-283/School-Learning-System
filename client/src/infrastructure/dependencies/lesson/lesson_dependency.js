const LessonRepositoryImpl = require("../../../infrastructure/repositories/lesson/lesson_repository_impl");

const SemesterLessonPlanRepositoryImpl = require("../../../infrastructure/repositories/lesson/semester_lesson_plan_repository_impl");

const SubjectLessonPlanRepositoryImpl = require("../../../infrastructure/repositories/lesson/subject_lesson_plan_repository_impl");

const CourseLessonPlanRepositoryImpl = require("../../../infrastructure/repositories/lesson/course_lesson_plan_repository_impl");

const ClassSectionLessonPlanRepositoryImpl = require("../../../infrastructure/repositories/lesson/class_section_lesson_plan_repository_impl");

const LessonPlanRepositoryImpl = require("../../../infrastructure/repositories/lesson/lesson_plan_repository_impl");
const lessonOpeningRepository = require("../../../infrastructure/repositories/lesson/lesson_opening_repository_impl");
const GetLessonsUseCase = require("../../../application/lessons/use_cases/get_lessons");
const CreateLessonUseCase = require("../../../application/lessons/use_cases/create_lesson");

const GetSemesterLessonPlansUseCase = require("../../../application/lessons/use_cases/get_semester_lesson_plans");
const CreateSemesterLessonPlansUseCase = require("../../../application/lessons/use_cases/create_semester_lesson_plans");

const GetSubjectLessonPlansUseCase = require("../../../application/lessons/use_cases/get_subject_lesson_plans");
const CreateSubjectLessonPlanUseCase = require("../../../application/lessons/use_cases/create_subject_lesson_plan");

const GetCourseLessonPlansUseCase = require("../../../application/lessons/use_cases/get_course_lesson_plans");

const GetClassSectionLessonPlansUseCase = require("../../../application/lessons/use_cases/get_class_section_lesson_plans");

const EnsureLessonPlansUseCase = require("../../../application/lessons/use_cases/ensure_lesson_plans");

const EnsureLessonOpeningsUseCase = require("../../../application/lessons/use_cases/ensure_lesson_openings");

const GetLessonOpeningsUseCase = require("../../../application/lessons/use_cases/get_lesson_openings");

// =========================================
// REPOSITORIES
// =========================================

const lessonRepository = new LessonRepositoryImpl();

const semesterLessonPlanRepository = new SemesterLessonPlanRepositoryImpl();

const subjectLessonPlanRepository = new SubjectLessonPlanRepositoryImpl();

const courseLessonPlanRepository = new CourseLessonPlanRepositoryImpl();

const classSectionLessonPlanRepository =
  new ClassSectionLessonPlanRepositoryImpl();
const lessonPlanRepository = new LessonPlanRepositoryImpl();

// =========================================
// USE CASES
// =========================================

const getLessonsUseCase = new GetLessonsUseCase(lessonRepository);

const createLessonUseCase = new CreateLessonUseCase(lessonRepository);

const getSemesterLessonPlansUseCase = new GetSemesterLessonPlansUseCase(
  semesterLessonPlanRepository,
);

const createSemesterLessonPlansUseCase = new CreateSemesterLessonPlansUseCase(
  semesterLessonPlanRepository,
);

const getSubjectLessonPlansUseCase = new GetSubjectLessonPlansUseCase(
  subjectLessonPlanRepository,
);

const createSubjectLessonPlanUseCase = new CreateSubjectLessonPlanUseCase(
  subjectLessonPlanRepository,
);

const getCourseLessonPlansUseCase = new GetCourseLessonPlansUseCase(
  courseLessonPlanRepository,
);

const getClassSectionLessonPlansUseCase = new GetClassSectionLessonPlansUseCase(
  classSectionLessonPlanRepository,
);

const ensureLessonPlansUseCase = new EnsureLessonPlansUseCase(
  lessonPlanRepository,
);
const ensureLessonOpeningsUseCase = new EnsureLessonOpeningsUseCase(
  lessonOpeningRepository,
);

const getLessonOpeningsUseCase = new GetLessonOpeningsUseCase(
  lessonOpeningRepository,
);
module.exports = {
  lessonRepository,
  getLessonsUseCase,
  createLessonUseCase,

  semesterLessonPlanRepository,
  getSemesterLessonPlansUseCase,
  createSemesterLessonPlansUseCase,

  subjectLessonPlanRepository,
  getSubjectLessonPlansUseCase,
  createSubjectLessonPlanUseCase,

  courseLessonPlanRepository,
  getCourseLessonPlansUseCase,

  classSectionLessonPlanRepository,
  getClassSectionLessonPlansUseCase,

  lessonPlanRepository,
  ensureLessonPlansUseCase,

  ensureLessonOpeningsUseCase,
  getLessonOpeningsUseCase,
};
