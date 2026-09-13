class GetActivesDepartmentsUseCase {

  constructor(departmentRepository) {
    this.departmentRepository =
      departmentRepository;
  }

  async execute(req) {

    return await this.departmentRepository
      .getActivesDepartments(req);
  }
}

module.exports =
  GetActivesDepartmentsUseCase;