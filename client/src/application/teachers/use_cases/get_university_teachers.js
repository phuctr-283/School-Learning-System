class GetUniversityTeachersUseCase {
  constructor(teacherRepository) {
    this.teacherRepository = teacherRepository;
  }

  async execute(req) {
    return await this.teacherRepository.getUniversityTeachers(req);
  }
}

module.exports = GetUniversityTeachersUseCase;
