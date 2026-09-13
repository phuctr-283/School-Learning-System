const CreateSubjectDTO = require("../dto/create_subject.dto");

class CreateSubjectUseCase {
  constructor(subjectRepository) {
    this.subjectRepository = subjectRepository;
  }

  async execute(req, data) {
    const dto = new CreateSubjectDTO(data);

    return await this.subjectRepository.createSubject(req, dto);
  }
}

module.exports = CreateSubjectUseCase;
