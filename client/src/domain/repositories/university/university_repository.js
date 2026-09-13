class UniversityRepository {
  async create(dto) {
    throw new Error(
      "UniversityRepository.create() chưa được implement"
    );
  }

  async getAll() {
    throw new Error(
      "UniversityRepository.getAll() chưa được implement"
    );
  }
  async getActiveUniversities() {

    throw new Error(
      "getActiveUniversities() must be implemented",
    );

  }
}

module.exports = UniversityRepository;