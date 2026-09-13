const SubjectRepositoryImpl = require("../../../infrastructure/repositories/subject/subject_repository_impl");

const GetSubjectsUseCase = require("../../../application/subjects/use_cases/get_subjects");
const CreateSubjectUseCase = require("../../../application/subjects/use_cases/create_subject");
const subjectRepository = new SubjectRepositoryImpl();

const getSubjectsUseCase = new GetSubjectsUseCase(subjectRepository);
const createSubjectUseCase = new CreateSubjectUseCase(subjectRepository);
module.exports = {
  subjectRepository,

  getSubjectsUseCase,
  createSubjectUseCase,
};
