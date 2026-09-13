class GetAssignmentsUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }

  async execute() {
    return this.assignmentRepository.getAssignments();
  }
}

module.exports = GetAssignmentsUseCase;