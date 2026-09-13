const RegisterTeacherDTO = require("../dto/register_teacher.dto");

class RegisterTeacherUseCase {
  constructor(teacherRepository) {
    this.teacherRepository = teacherRepository;
  }

  async execute(data) {
    const dto = new RegisterTeacherDTO(data);

    return await this.teacherRepository.registerTeacher(dto);
  }
}

module.exports = RegisterTeacherUseCase;
