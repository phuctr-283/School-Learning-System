class GetUniversitiesUseCase {

  constructor(universityRepository) {
    this.universityRepository =
      universityRepository;
  }

  async execute(req) {

    return this.universityRepository.getAll(
      req
    );
  }
}

module.exports = GetUniversitiesUseCase;