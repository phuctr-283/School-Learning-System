class CreateSubjectDTO {
  constructor(data = {}) {
    this.subjectId = data.subject_id;

    this.name = data.name;

    this.departmentId = data.department_id;

    this.subjectTypes = data.subject_types;

    this.credits = data.credits;

    this.processPercent = data.process_percent;

    this.midtermPercent = data.midterm_percent;

    this.finalPercent = data.final_percent;
  }

  toJSON() {
    return {
      subject_id: this.subjectId,

      name: this.name,

      department_id: this.departmentId,

      subject_types: this.subjectTypes,

      credits: this.credits,

      process_percent: this.processPercent,

      midterm_percent: this.midtermPercent,

      final_percent: this.finalPercent,
    };
  }
}

module.exports = CreateSubjectDTO;
