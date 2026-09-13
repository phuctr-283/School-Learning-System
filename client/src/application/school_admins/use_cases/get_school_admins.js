class GetSchoolAdminsUseCase {
  constructor(schoolAdminRepository) {
    this.schoolAdminRepository = schoolAdminRepository;
  }

  async execute(req) {
    return this.schoolAdminRepository.getAll(req);
  }
}

module.exports = GetSchoolAdminsUseCase;
