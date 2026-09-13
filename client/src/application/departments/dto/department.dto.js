class DepartmentDTO {
  constructor({
    department_id,
    department_number,
    name,
    university_id,
    university_name,
    head_id,
    head_name,
    is_active,
  }) {
    this.departmentId = department_id;

    this.departmentNumber = department_number;

    this.name = name;

    this.universityId = university_id;

    this.universityName = university_name;

    this.headId = head_id ?? null;

    this.headName = head_name ?? null;

    this.isActive = is_active;
  }
}

module.exports = DepartmentDTO;
