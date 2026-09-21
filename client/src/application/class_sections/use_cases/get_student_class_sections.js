class GetStudentClassSectionsUseCase {
  constructor(studentRepository) {
    this.studentRepository = studentRepository;
  }

  async execute(req) {
    return this.studentRepository.getStudentClassSections(req);
  }
}

module.exports = GetStudentClassSectionsUseCase;