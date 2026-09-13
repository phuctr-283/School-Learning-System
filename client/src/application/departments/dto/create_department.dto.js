class CreateDepartmentDTO {
  constructor({
    department_id,
    department_number,
    name,
    head_id,
  }) {
    this.departmentId =
      department_id?.trim().toUpperCase();

    this.departmentNumber =
      department_number?.trim();

    this.name =
      name?.trim();

    this.headId =
      head_id?.trim() || null;
  }
}

module.exports = CreateDepartmentDTO;