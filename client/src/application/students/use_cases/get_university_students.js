class GetUniversityStudentsUseCase {
  constructor(studentRepository) {
    this.studentRepository = studentRepository;
  }

  async execute(req) {
    return await this.studentRepository.getUniversityStudents(req);
  }
}

module.exports = GetUniversityStudentsUseCase;
