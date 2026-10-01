const UpdateAssignmentDTO = require("../dto/update_assignment.dto");

class UpdateAssignmentUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }

  async execute(req, input) {
    const dto = new UpdateAssignmentDTO(input);

    return this.assignmentRepository.updateAssignment(req, dto);
  }
}

module.exports = UpdateAssignmentUseCase;
