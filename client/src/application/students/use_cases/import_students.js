class ImportStudentsUseCase {
  constructor(studentRepository) {
    this.studentRepository = studentRepository;
  }

  async execute(req, file) {
    return await this.studentRepository.importStudents(req, file);
  }
}

module.exports = ImportStudentsUseCase;
