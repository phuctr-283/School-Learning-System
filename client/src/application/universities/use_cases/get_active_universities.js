class GetActiveUniversitiesUseCase {
  constructor(universityRepository) {
    this.universityRepository = universityRepository;
  }

  async execute() {
    return await this.universityRepository.getActiveUniversities();
  }
}

module.exports = GetActiveUniversitiesUseCase;
