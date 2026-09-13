class StudentDTO {
  constructor(data = {}) {
    this.studentId = data.student_id;

    this.fullName = data.full_name;

    this.gender = data.gender;

    this.studentClass = data.student_class;

    this.departmentId = data.department_id;

    this.departmentName = data.department_name;

    this.cohortId = data.cohort_id;

    this.status = data.status;

    this.universityId = data.university_id;

    this.universityName = data.university_name;

    this.dateOfBirth = data.date_of_birth;

    this.email = data.email;

    this.phone = data.phone;
  }
}

module.exports = StudentDTO;
