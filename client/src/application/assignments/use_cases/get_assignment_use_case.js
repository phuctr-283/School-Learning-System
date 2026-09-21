class GetAssignmentUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }

  async execute(req, assignmentId) {
    if (!assignmentId) {
      throw new Error("Thiếu mã bài tập.");
    }

    return await this.assignmentRepository.getAssignmentById(req, assignmentId);
  }
}

module.exports = GetAssignmentUseCase;
