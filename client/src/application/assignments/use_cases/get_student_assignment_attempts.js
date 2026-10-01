class GetStudentAssignmentAttemptsUseCase {
  constructor(repository) {
    this.repository = repository;
  }

  async execute(req, { assignmentApplicationId, classSectionId, lessonId }) {
    return this.repository.getStudentAssignmentAttempts(req, {
      assignmentApplicationId,
      classSectionId,
      lessonId,
    });
  }
}

module.exports = GetStudentAssignmentAttemptsUseCase;
