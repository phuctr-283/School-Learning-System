const StudentRepositoryImpl = require("../../repositories/student/student_repository_impl");

const GetUniversityStudentsUseCase = require("../../../application/students/use_cases/get_university_students");
const ImportStudentsUseCase = require("../../../application/students/use_cases/import_students");

const studentRepository = new StudentRepositoryImpl();

const getUniversityStudentsUseCase = new GetUniversityStudentsUseCase(
  studentRepository,
);
const importStudentsUseCase = new ImportStudentsUseCase(studentRepository);

module.exports = {
  studentRepository,

  getUniversityStudentsUseCase,
  importStudentsUseCase,
};
