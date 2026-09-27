class SubmitStudentAssignmentUseCase {
  constructor(repository) {
    this.repository = repository;
  }

  async execute(params) {
    return this.repository.submitAssignment({
      student_id: params.studentId,
      assignment_application_id: params.assignmentApplicationId,
      class_section_id: params.classSectionId,
      lesson_id: params.lessonId,
      attempt_id: params.attemptId,
      answers: params.answers || {},
    });
  }
}

module.exports = SubmitStudentAssignmentUseCase;
