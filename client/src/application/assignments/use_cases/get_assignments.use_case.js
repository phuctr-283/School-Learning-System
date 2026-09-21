class GetAssignmentsUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }

  async execute(req) {
    return await this.assignmentRepository.getAssignments(
      req,
    );
  }
}

module.exports = GetAssignmentsUseCase;