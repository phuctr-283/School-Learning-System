class GetSemestersUseCase {

  constructor(
    semesterRepository,
  ) {

    this.semesterRepository =
      semesterRepository;
  }

  async execute(req) {

    return await this.semesterRepository
      .getUniversitySemesters(req);
  }
}

module.exports = GetSemestersUseCase;