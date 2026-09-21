const CreateAssignmentDTO = require(
  "../dto/create_assignment.dto.js",
);


class CreateAssignmentUseCase {
  constructor(assignmentRepository) {
    this.assignmentRepository = assignmentRepository;
  }


  async execute(req, input) {
    const dto = new CreateAssignmentDTO(input);

    return this.assignmentRepository.createAssignment(
      req,
      dto,
    );
  }
}


module.exports = CreateAssignmentUseCase;