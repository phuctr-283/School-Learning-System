class CreateAssignmentDTO {
  constructor({
    subjectId,
    title,
    description = null,
    assignmentType = "practice",
    questions = [],
  }) {
    this.subjectId = subjectId;
    this.title = title;
    this.description = description;
    this.assignmentType = assignmentType;
    this.questions = questions;
  }

  toRequestBody() {
    return {
      subject_id: this.subjectId,
      title: this.title,
      description: this.description,
      assignment_type: this.assignmentType,
      questions: this.questions,
    };
  }
}

module.exports = CreateAssignmentDTO;