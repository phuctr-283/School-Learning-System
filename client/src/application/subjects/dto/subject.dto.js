class SubjectDTO {
  constructor(data = {}) {
    this.subjectId = data.subject_id;
    this.name = data.name;

    this.universityId = data.university_id;
    this.universityName = data.university_name;

    this.departmentId = data.department_id;
    this.departmentName = data.department_name;

    this.subjectTypes = data.subject_types;

    this.credits = data.credits;

    this.processPercent = data.process_percent;
    this.midtermPercent = data.midterm_percent;
    this.finalPercent = data.final_percent;

    this.status = data.status;
  }
}

module.exports = SubjectDTO;