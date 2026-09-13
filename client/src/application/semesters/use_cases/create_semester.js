const CreateSemesterDTO = require("../dto/create_semester.dto");

class CreateSemesterUseCase {
  constructor(semesterRepository) {
    this.semesterRepository = semesterRepository;
  }

  async execute(req, data) {
    const dto = new CreateSemesterDTO(data);

    return await this.semesterRepository.createSemester(req, dto);
  }
}

module.exports = CreateSemesterUseCase;
