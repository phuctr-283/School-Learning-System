class GetUniversityDepartmentsUseCase {
  constructor(departmentRepository) {
    this.departmentRepository = departmentRepository;
  }

  async execute(req) {
    return await this.departmentRepository.getUniversityDepartments(req);
  }
}

module.exports = GetUniversityDepartmentsUseCase;
