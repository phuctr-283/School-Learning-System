class GetAssignmentByIdUseCase {

  constructor(
    assignmentRepository,
  ) {
    this.assignmentRepository =
      assignmentRepository;
  }

  async execute(
    req,
    assignmentId,
  ) {

    const id = String(
      assignmentId ?? "",
    ).trim();

    if (!id) {
      throw new Error(
        "Thiếu mã bài tập.",
      );
    }

    return this.assignmentRepository
      .getAssignmentById(
        req,
        id,
      );
  }
}

module.exports =
  GetAssignmentByIdUseCase;