class GetTeacherActiveSubjectsUseCase {

  constructor(classSectionRepository) {
    this.classSectionRepository =
      classSectionRepository;
  }

  async execute(req) {
    return await this.classSectionRepository
      .getTeacherActiveSubjects(req);
  }
}

module.exports = GetTeacherActiveSubjectsUseCase;