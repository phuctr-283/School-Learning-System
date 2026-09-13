class GetActivePlannedSemestersUseCase {
  constructor(semesterRepository) {
    this.semesterRepository = semesterRepository;
  }

  async execute(req) {
    return await this.semesterRepository.getActivePlanned(req);
  }
}

module.exports = GetActivePlannedSemestersUseCase;
