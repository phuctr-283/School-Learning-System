class ActiveDepartmentDTO {
  constructor({ department_id, department_number, name }) {
    this.departmentId = department_id;

    this.departmentNumber = department_number;

    this.name = name;
  }
}

module.exports = ActiveDepartmentDTO;
