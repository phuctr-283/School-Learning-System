const ApplyAssignmentDTO = require("../dto/apply_assignment.dto");

class ApplyAssignmentUseCase {
  constructor(assignmentApplicationRepository) {
    this.assignmentApplicationRepository = assignmentApplicationRepository;
  }

  async execute(req, input) {
    const dto =
      input instanceof ApplyAssignmentDTO
        ? input
        : ApplyAssignmentDTO.fromRequest(input);

    dto.validate();

    return await this.assignmentApplicationRepository.applyAssignment(req, dto);
  }
}

module.exports = ApplyAssignmentUseCase;
