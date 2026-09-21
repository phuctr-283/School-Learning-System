class TeacherSubjectDTO {
  constructor({
    university_id,
    department_id,
    subject_id,
    subject_name,
  }) {
    this.universityId = university_id ?? "";
    this.departmentId = department_id ?? "";
    this.subjectId = subject_id ?? "";
    this.subjectName = subject_name ?? "";
  }

  static fromResponse(data) {
    return new TeacherSubjectDTO(data);
  }
}

module.exports = TeacherSubjectDTO;