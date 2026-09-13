const TeacherRepositoryImpl = require(
  "../../repositories/teacher/teacher_repository_impl",
);

const GetUniversityTeachersUseCase = require(
  "../../../application/teachers/use_cases/get_university_teachers",
);

const RegisterTeacherUseCase = require(
  "../../../application/teachers/use_cases/register_teacher",
);


// Repository
const teacherRepository =
  new TeacherRepositoryImpl();


// Use cases
const getUniversityTeachersUseCase =
  new GetUniversityTeachersUseCase(
    teacherRepository,
  );

const registerTeacherUseCase =
  new RegisterTeacherUseCase(
    teacherRepository,
  );


// Export
module.exports = {
  teacherRepository,

  getUniversityTeachersUseCase,
  registerTeacherUseCase,
};