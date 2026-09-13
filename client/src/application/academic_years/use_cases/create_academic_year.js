const CreateAcademicYearDTO = require("../dto/create_academic_year.dto");

class CreateAcademicYearUseCase {
  constructor(academicYearRepository) {
    this.academicYearRepository = academicYearRepository;
  }

  async execute(req, data) {
    const dto = new CreateAcademicYearDTO(data);

    return await this.academicYearRepository.createAcademicYear(req, dto);
  }
}

module.exports = CreateAcademicYearUseCase;
