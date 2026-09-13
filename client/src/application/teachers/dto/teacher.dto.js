class TeacherDTO {
  constructor({
    teacher_id,
    full_name,
    gender,
    date_of_birth,
    email,
    phone,
    department_id,
    department_name,
    university_id,
    university_name,
    status,
  }) {
    this.teacherId = teacher_id;

    this.fullName = full_name;

    this.gender = gender ?? null;

    this.dateOfBirth = date_of_birth ?? null;

    this.email = email ?? null;

    this.phone = phone ?? null;

    this.departmentId = department_id;

    this.departmentName = department_name;

    this.universityId = university_id;

    this.universityName = university_name;

    this.status = status;
  }
}

module.exports = TeacherDTO;
