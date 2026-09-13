const CreateDepartmentDTO = require("../dto/create_department.dto");

class CreateDepartmentUseCase {
  constructor(departmentRepository) {
    this.departmentRepository = departmentRepository;
  }

  async execute(req, data) {
    const dto = new CreateDepartmentDTO(data);

    // =========================================
    // VALIDATION
    // =========================================

    if (!dto.departmentId) {
      throw new Error("Mã khoa không được để trống");
    }

    if (!dto.departmentNumber) {
      throw new Error("Số khoa không được để trống");
    }

    if (!dto.name) {
      throw new Error("Tên khoa không được để trống");
    }

    // =========================================
    // CREATE
    // =========================================

    return await this.departmentRepository.create(req, dto);
  }
}

module.exports = CreateDepartmentUseCase;
