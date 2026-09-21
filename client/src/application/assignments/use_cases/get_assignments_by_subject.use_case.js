class GetAssignmentsBySubjectUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }

  async execute(req, subjectId) {
    return await this.assignmentRepository
      .getAssignmentsBySubject(
        req,
        subjectId,
      );
  }
}

module.exports = GetAssignmentsBySubjectUseCase;