class GetActiveDepartmentsUseCase {
  constructor(departmentRepository) {
    this.departmentRepository = departmentRepository;
  }

  async execute(universityId) {
    if (!universityId) {
      throw new Error("Chưa chọn trường đại học");
    }

    return await this.departmentRepository.getActiveDepartments(universityId);
  }
}

module.exports = GetActiveDepartmentsUseCase;
