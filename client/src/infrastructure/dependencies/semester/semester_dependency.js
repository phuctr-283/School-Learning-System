const SemesterRepositoryImpl = require("../../repositories/semester/semester_repository_impl");

const GetSemestersUseCase = require("../../../application/semesters/use_cases/get_semesters");
const GetActivePlannedSemestersUseCase =
  require(
    "../../../application/semesters/use_cases/get_active_planned_semesters"
  );
const CreateSemesterUseCase = require("../../../application/semesters/use_cases/create_semester");

const semesterRepository = new SemesterRepositoryImpl();

const getSemestersUseCase = new GetSemestersUseCase(semesterRepository);
const getActivePlannedSemestersUseCase = new GetActivePlannedSemestersUseCase(semesterRepository);
const createSemesterUseCase = new CreateSemesterUseCase(semesterRepository);

module.exports = {
  semesterRepository,

  getSemestersUseCase,
  getActivePlannedSemestersUseCase,
  createSemesterUseCase,
};
