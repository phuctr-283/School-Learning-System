const CreateAssignmentDTO = require(
  "../dto/create_assignment.dto",
);

class CreateAssignmentUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }

  async execute(input) {
    const dto = new CreateAssignmentDTO(input);

    if (!dto.title?.trim()) {
      throw new Error(
        "Tiêu đề bài tập không được để trống",
      );
    }

    if (!dto.subjectId) {
      throw new Error(
        "Chưa chọn môn học",
      );
    }

    if (
      !Array.isArray(dto.questions) ||
      dto.questions.length === 0
    ) {
      throw new Error(
        "Danh sách câu hỏi không được để trống",
      );
    }

    return this.assignmentRepository.createAssignment(dto);
  }
}

module.exports = CreateAssignmentUseCase;