const AcademicYearRepositoryImpl = require("../../repositories/academic_year/academic_year_repository_impl");

const GetActiveAndPlannedAcademicYearsUseCase = require("../../../application/academic_years/use_cases/get_active_and_planned_academic_years");

const GetAcademicYearsUseCase = require("../../../application/academic_years/use_cases/get_academic_years");

const CreateAcademicYearUseCase = require("../../../application/academic_years/use_cases/create_academic_year");

const academicYearRepository = new AcademicYearRepositoryImpl();

const getActiveAndPlannedAcademicYearsUseCase =
  new GetActiveAndPlannedAcademicYearsUseCase(academicYearRepository);

const getAcademicYearsUseCase = new GetAcademicYearsUseCase(
  academicYearRepository,
);

const createAcademicYearUseCase = new CreateAcademicYearUseCase(
  academicYearRepository,
);

module.exports = {
  academicYearRepository,

  getActiveAndPlannedAcademicYearsUseCase,
  getAcademicYearsUseCase,
  createAcademicYearUseCase,
};
