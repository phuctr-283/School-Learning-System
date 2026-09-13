const UniversityRepositoryImpl = require(
  "../../repositories/university/university_repository_impl",
);

const GetUniversitiesUseCase = require(
  "../../../application/universities/use_cases/get_universities",
);

const GetActiveUniversitiesUseCase = require(
  "../../../application/universities/use_cases/get_active_universities",
);

const CreateUniversityUseCase = require(
  "../../../application/universities/use_cases/create_university",
);


// Repository dùng chung cho các university use case
const universityRepository =
  new UniversityRepositoryImpl();


// Use cases
const getUniversitiesUseCase =
  new GetUniversitiesUseCase(
    universityRepository,
  );

const getActiveUniversitiesUseCase =
  new GetActiveUniversitiesUseCase(
    universityRepository,
  );

const createUniversityUseCase =
  new CreateUniversityUseCase(
    universityRepository,
  );


// Export
module.exports = {
  universityRepository,

  getUniversitiesUseCase,
  getActiveUniversitiesUseCase,
  createUniversityUseCase,
};