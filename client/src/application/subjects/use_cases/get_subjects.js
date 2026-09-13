class GetSubjectsUseCase {

  constructor(subjectRepository) {
    this.subjectRepository =
      subjectRepository;
  }

  async execute(req) {

    return await this.subjectRepository
      .getUniversitySubjects(req);
  }
}

module.exports =
  GetSubjectsUseCase;